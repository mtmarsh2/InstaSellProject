# Create your views here.
from nexmo import send_message
from django.core.files import File
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template.context import RequestContext
from .models import SellPost
import sys
import os
from mezzanine.conf import settings
from django.utils import simplejson
from django.core.files.storage import default_storage
from settings import MEDIA_URL, STATIC_URL, SELLPOST_EXTENSION, SITE_TAG, ACCESS_TOKEN, NEXMO_USERNAME, NEXMO_PASSWORD, NEXMO_FROM, API_KEY, API_SECRET,YOUR_NUMBER
from django.core.exceptions import ObjectDoesNotExist 
from django.db.models import Q
from instagram.client import InstagramAPI
from django.contrib.auth.models import User
import datetime
from newaccounts.models import UserProfile


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


#this is the homepage view
def index(request):
    send_message('+16302071793', 'marshall message')
    posts = getSellPosts()
    print len(posts) or "Its none"
    updateSellPosts(posts)
    sellposts = SellPost.objects.all()[:12]
    print SITE_TAG
    return render_to_response('sellposts/index.html', {'sellposts': sellposts}, context_instance = RequestContext(request))

#uses instagram api to get pull all instagram posts with @InstaSell. If sellpost already with title, skip over and do not make another sellpost
def getSellPosts():
    from instagram.client import InstagramAPI
    api = InstagramAPI(access_token = ACCESS_TOKEN)
    middle = []
    print SITE_TAG + "The sitetag"
    middle = api.tag_recent_media(tag_name = SITE_TAG)
    final = []
    print middle[0] 
    for item in middle[0]:
        for tag in item.tags:
		if tag.name == SITE_TAG:
		    newelem = {}
		    newelem['image'] = item.images['standard_resolution']
		    newelem['user'] = item.user.username
		    caption = str(item.caption.text)
		    newelem['title'] = caption[:(caption.find('#'))]
		    newelem['description'] = item.caption
		    newelem['time'] = item.created_time
		    final.append(newelem)
		    #this makes sure no post is added twice 
		    break
    return final

def updateSellPosts(postslist = None):
    import urllib
    if postslist is None or len(postslist) == 0:
        return
    for post in postslist:
        if post is not None:
	    print post['title'] + 'title'
	    try: 
                spot = SellPost.objects.get(title = post['title'])
		print 'try worked'
	        pass
	    except ObjectDoesNotExist:
		 print 'exception'
	         try:
		     user = User.objects.get(username = post['user'])
		     userprof = UserProfile.objects.get(user = user)
		     #grab image from url
		     nm = os.path.basename(post['image'].url)
		     fname, fext = os.path.splitext(nm)
		     urllib.urlretrieve(post['image'].url, fname + fext)
		     im = Image.open(fname+fext)
		     im.save("static/media/" + fname + fext)
		     print type(post['image'])
		     print dir(post['image'])
		     newsellpost = SellPost(user = userprof, description = post['description'], time = post['time'], title = post['title'])
		     newsellpost.image.save('', File(open(nm), 'rb'), False)
		     newsellpost.save()
		     print "okeay"
	         except ObjectDoesNotExist:
		     print "damn"
		     pass
    return 

def handle_incoming_message(request):
    if request.method == "GET":
        #run through attributes
	user_to = request['to']
	user_from = request['msisdn']
	text = request['text']
	handle_outgoing_message(user_to = user_to, user_from = user_from, text = text)
	#m = Message(user_to = user_to, user_from = user_from, message = text)
	#m.save()
    return HttpResponse(200)

def handle_outgoing_message(request):
    return

def generate_number():
    return YOUR_NUMBER

def render_individual_sellpost(request, path_to_image):
    #strip .thumbnails part of filepath if its there
    nextmo_number = generate_number()
    try:
        sellpost = SellPost.objects.get(image = "images/" + str(path_to_image))
    except ObjectDoesNotExist:
        return 404
    return render_to_response('sellposts/individualsellpost.html', {'sellpost': sellpost, 'netmo_number': nextmo_number}, context_instance = RequestContext(request))

def search(request):
    results = SellPost.objects.none() 
    query = request.GET['q']
    search_terms = query.split()
    for term in search_terms:
        results = SellPost.objects.filter(Q(title__icontains = term) | Q(tags = SellPost.tags.filter(name__icontains=term))).distinct()
    return render_to_response('sellposts/searchresults.html', {'results':results, 'query': query}, context_instance = RequestContext(request))

