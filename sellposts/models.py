from django.db import models
from django.utils import timezone
import datetime
from datetime import *
from newaccounts.models import UserProfile
from taggit.managers import TaggableManager
from django.db.models import Avg, Count
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from settings import MEDIA_URL, STATIC_URL, SELLPOST_EXTENSION
import sys
import os
from mezzanine.conf import settings
from django.core.files.storage import default_storage

try:
    from urllib.request import urlopen
    from urllib.parse import urlencode, quote, unquote
except ImportError:
    from urllib import urlopen, urlencode, quote, unquote

try:
    from json import loads
except ImportError:  # Python < 2.6
    from django.utils.simplejson import loads

# Try to import PIL in either of the two ways it can end up installed.
try:
	from PIL import Image, ImageFile, ImageOps
except ImportError:
    import Image
    import ImageFile
    import ImageOps


class SellPost(models.Model):
    title = models.CharField(max_length = 20)
    description = models.TextField()
    user = models.ForeignKey(UserProfile)
    tags = TaggableManager()
    time = models.DateTimeField(auto_now_add = False)

    #returns current time used for path to store image
    def getCurrentTime(self):
        currtime = datetime.now()
        return str(currtime.year) + str(currtime.month) + str(currtime.day) + str(currtime.hour) + str(currtime.minute) + str(currtime.second) + str(currtime.microsecond)

    def getPath(instance, filename):
        return SELLPOST_EXTENSION + instance.getCurrentTime() + ".jpg"

    #upload_to must be a callable, else filename will be used in the path where the image is saved to
    image = models.ImageField(upload_to = getPath)

    def __unicode__(self):
        return str(self.title)

def create_thumbnail(sender, instance, created, **kwargs):
    if created:
        thumbnail(instance.image.url, 300, 300)

        
post_save.connect(create_thumbnail, sender = SellPost)

def thumbnail(image_url, width, height, quality=95):
    """
    Given the URL to an image, resizes the image using the given width and
    height on the first time it is requested, and returns the URL to the new
    resized image. if width or height are zero then original ratio is
    maintained.
    """
    if not image_url:
        return ""

    image_url = unquote(str(image_url)).split("?")[0]
    if image_url.startswith(settings.MEDIA_URL):
        image_url = image_url.replace(settings.MEDIA_URL, "", 1)
    image_dir, image_name = os.path.split(image_url)
    image_prefix, image_ext = os.path.splitext(image_name)
    filetype = {".png": "PNG", ".gif": "GIF"}.get(image_ext, "JPEG")
    thumb_name = "%s%s" % (image_prefix, image_ext)
    thumb_dir = os.path.join(settings.MEDIA_ROOT, image_dir,
                             settings.THUMBNAILS_DIR_NAME)

    if not os.path.exists(thumb_dir):
        os.makedirs(thumb_dir)
    thumb_path = os.path.join(thumb_dir, thumb_name)
    thumb_url = "%s/%s" % (settings.THUMBNAILS_DIR_NAME,
                           quote(thumb_name.encode("utf-8")))
    image_url_path = os.path.dirname(image_url)
    if image_url_path:
        thumb_url = "%s/%s" % (image_url_path, thumb_url)

    try:
        thumb_exists = os.path.exists(thumb_path)
    except UnicodeEncodeError:
        # The image that was saved to a filesystem with utf-8 support,
        # but somehow the locale has changed and the filesystem does not
        # support utf-8.
        from mezzanine.core.exceptions import FileSystemEncodingChanged
        raise FileSystemEncodingChanged()
    if thumb_exists:
        # Thumbnail exists, don't generate it.
        return thumb_url
    elif not default_storage.exists(image_url):
        # Requested image does not exist, just return its URL.
        return image_url

    f = default_storage.open(image_url)
    try:
        image = Image.open(f)
    except:
        # Invalid image format
        return image_url

    image_info = image.info
    width = int(width)
    height = int(height)

    # If already right size, don't do anything.
    if width == image.size[0] and height == image.size[1]:
        return image_url
    # Set dimensions.
    if width == 0:
        width = image.size[0] * height // image.size[1]
    elif height == 0:
        height = image.size[1] * width // image.size[0]
    if image.mode not in ("P", "L", "RGBA"):
        image = image.convert("RGBA")
    # Required for progressive jpgs.
    ImageFile.MAXBLOCK = 2 * (max(image.size) ** 2)
    try:
    	size = width, height
    	image = image.resize(size, Image.ANTIALIAS)
    	image.save(thumb_path, filetype, quality=quality, **image_info)
        # Push a remote copy of the thumbnail if MEDIA_URL is
        # absolute.
        if "://" in settings.MEDIA_URL:
            with open(thumb_path, "r") as f:
                default_storage.save(thumb_url, File(f))
    except Exception:
        # If an error occurred, a corrupted image may have been saved,
        # so remove it, otherwise the check for it existing will just
        # return the corrupted image next time it's requested.
        try:
            os.remove(thumb_path)
        except Exception:
            pass
        return image_url
    return thumb_url
