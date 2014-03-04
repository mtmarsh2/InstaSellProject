from django.db import models
from django.contrib.auth.models import User
from django.db.models import signals
from newaccounts.signals import create_profile
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from settings import MEDIA_URL, STATIC_URL, PROJECT_ROOT
from django.db.models.fields.files import ImageFieldFile, FileField
from PIL import Image
import hashlib
import random
import re
from django.contrib.sites.models import Site
from django.template.loader import render_to_string

DEFAULT_PROFILE_IMAGE_PATH = PROJECT_ROOT + STATIC_URL + 'instaselllogo.png'
#Added to make sure user email field is unique


class UserProfile(models.Model):
    user = models.OneToOneField(User)
    email_address = models.EmailField(default="")
    profilepicture = models.ImageField(upload_to="profilepictures/")


    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            instance.save()
            new_userprofile = UserProfile.objects.create(user=instance)

    #overide save to add default image if user does not specify pic
    #also add user_activation key if none exists
    def save(self, *args, **kwargs):
        if not self.profilepicture:
            im = Image.open(DEFAULT_PROFILE_IMAGE_PATH)
            full_path = PROJECT_ROOT + MEDIA_URL + 'profilepictures/' + self.user.username + '.png'
	    print full_path + " :This is the fullpath\n"
            im.save( full_path, 'PNG')
            short_path = 'profilepictures/' + self.user.username + '.png'
            self.profilepicture = ImageFieldFile(instance = None, name = short_path, field = FileField())

        super(UserProfile, self).save(*args, **kwargs)

    post_save.connect(create_user_profile, sender=User)

    def __unicode__(self):
    	return str(self.user)

class Message(models.Model):
	message_text = models.CharField(max_length = 50)
	user_to = models.ForeignKey(UserProfile, related_name="user_to")
	user_from = models.ForeignKey(UserProfile, related_name="user_from")
	time = models.DateTimeField(auto_now_add = True)
   
