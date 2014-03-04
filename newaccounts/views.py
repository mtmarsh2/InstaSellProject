# Create your views here.
from django.shortcuts import render_to_response, render
from django.http import HttpResponse, HttpResponseBadRequest
from django.template.context import RequestContext
from django.core.mail import send_mail
from django.http import HttpResponseRedirect
from django import forms
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from django.contrib.auth import login as auth_login
from django.contrib.auth import authenticate
from django.contrib.auth import logout, logout
from newaccounts.forms import Email_Change_Form
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
import urllib2
import urllib
from models import UserProfile
from forms import UserCreateForm
from sellposts.forms import SellPostForm
from sellposts.models import SellPost 
import json
from json import *
from settings import STATIC_URL, PROJECT_ROOT
from PIL import Image
from django.db.models.fields.files import ImageFieldFile, FileField
from settings import SELLPOST_EXTENSION, MEDIA_ROOT
import os
from django.core.files import File
import simplejson
from django.core.urlresolvers import reverse
from .forms import UserCreateForm


def register(request):
    register_success = reverse('user_register_success')
    if request.method == 'POST':
		form = UserCreateForm(request.POST)
		if form.is_valid():
			form.save()
			return HttpResponseRedirect(register_success)
    else:
		form = UserCreateForm()
    return render_to_response('newaccounts/registration.html', {'form':form}, context_instance=RequestContext(request))

#The page the user is redirected to once they sign up
def user_register_success(request):
    return render_to_response('newaccounts/register_success.html', context_instance = RequestContext(request))


def delete_image(request, pic_id):
	a = request.user
	image = User_Image.objects.get(id=pic_id)
	image.delete()
	return HttpResponseRedirect("/accounts/profile/%s" % a)
	
def edit_image(request, pic_id):
	image = User_Image.objects.get(id=pic_id)
	form = User_Image_EditForm(instance=image)
	done = False
	if request.method == 'POST':
		form = User_Image_EditForm(request.POST, instance=image)
		if form.is_valid():
			form.save()
			done = True
	else:
		form = User_Image_EditForm()
	return render_to_response('edit_image.html', {'form':form, 'image':image, 'done':done}, context_instance=RequestContext(request))

def display_user_images(request, profile_of_user):
	a = request.user
	check = False
	if str(a) == str(profile_of_user):
		check = True
	username_of_requested = User.objects.get(username=profile_of_user)
	requested_user_profile = UserProfile.objects.get(user=username_of_requested)
	images = User_Image.objects.filter(user_profile=requested_user_profile)
	return render_to_response("my_images.html", {'images':images, 'check':check}, context_instance=RequestContext(request))

def upload_image(request):
	done = False
	if request.method == 'POST':
		form = User_ImageForm(request.POST, request.FILES)
		if form.is_valid():
			form.save()
			image = User_Image.objects.get(title=form.cleaned_data['title'])
			a = str(image.image.url)
			img = Image.open("media/%s" % a)
			img = img.resize((200,200), PIL.Image.ANTIALIAS)
			img.save("media/resized/%s" % a)
			done = True
	return render_to_response('uploadimage.html', {'form':form, 'done':done}, context_instance=RequestContext(request))

def testing(request):
	dictionary = []
	images = User_Image.objects.all()
	for image in images:
		a = str(image.image.url)
		img = Image.open("media/%s" % a)
		img = img.resize((200,200), PIL.Image.ANTIALIAS)
		img.save("media/%s" % a)
	return render_to_response("ind.html", {'images':images}, context_instance=RequestContext(request))

def profile(request, name):
    from django.middleware.csrf import get_token
    csrf_token = get_token(request)
    name_of_current_user = str(request.user.username)
    profile_username = str(name)
    profiledict = {}
    user = User.objects.get(username = name)
    user_profile = UserProfile.objects.get(user = user)
    #check if user is on his own profile page
    if profile_username == name_of_current_user:
    	profiledict['same_user'] = True 
    else:
    	pass
    profiledict['user_profile'] = user_profile
    profiledict['form'] = SellPostForm()
    profiledict['csrf_token'] = csrf_token
    return render_to_response("newaccounts/profile.html", profiledict, context_instance=RequestContext(request))

#uploads sellpost from user, accepts both ajax/post or just post
def uploadsellpostture(request):
    if( request.is_ajax() and request.method == "POST"):
        form = SellPostForm(request.POST)
        if form.is_valid():
            image_path = request.POST['image_path']
            #image_path = '/static/media/uploads/cool-blue-room1.jpg'
            #get filename from image_path
            image_filename = os.path.basename(image_path)
            #get type of image (ex. .jpg) + name
            fname, fext =  os.path.splitext(image_filename)
            #last / of static_url isnt needed since provided by image_path
            im = Image.open(PROJECT_ROOT + image_path)
            #save image to correct spot from temp path
            im.save(MEDIA_ROOT + '/' + SELLPOST_EXTENSION + image_filename)
            newsellpost = form.save(commit = False)
            #lookup user
            user = UserProfile.objects.get(user = request.user)
            newsellpost.user = user
            newsellpost.image.save( '', File(open(PROJECT_ROOT + image_path, 'rb')), False)
            newsellpost.save()
            form.save_m2m()
            return HttpResponse('the form was not valid')
        else:
            data = {}
            for key in form.errors:
                data[key] = form.errors[key][0]

            data = simplejson.dumps(data)
            return HttpResponseBadRequest(data, mimetype = 'application/json')
    else:
        form = SellPostForm(request.POST)
        assert False
        #create new sellpost object from form, but don't save yet since we need to add user
        newsellpost = form.save(commit = False)
        #lookup user
        user = UserProfile.objects.get(user = request.user)
        newsellpost.user = user
        newsellpost.save()
        form.save_m2m()
    return HttpResponse('helloi')



def profile_search(request):
	errors = []
	profile = ""
	if 'q' in request.GET:
	    q=request.GET['q']
	    if q is None:
	    	errors.append('Enter a search term!')
	    else:
			try: 
				pro = User.objects.get(username__exact=q)
				return HttpResponseRedirect("/accounts/profile/%s" % q)
			except ObjectDoesNotExist:
				errors.append('The user you searched for does not exist, please enter a valid username')
	return render_to_response("profile_search.html" , {'errors':errors, 'profile':profile}, context_instance=RequestContext(request))

def email_change(request):
    email_change_done = reverse('email_change_done')
    errors = []
    form = Email_Change_Form()
    if request.method=='POST':
        form = Email_Change_Form(request.POST)
        if form.cleaned_data['email1']  == form.cleaned_data['email2']:
            if form.is_valid():
                u = User.objects.get(username=request.user)
                # get the proper user
                u.email = form.cleaned_data['email1'] 
                #^this is where the error is thrown
                u.save()
                return HttpResponseRedirect(email_change_done)
            else:
                for key in form.errors:
                    data[key] = form.errors[key][0]
                data = simplejson.dumps(data)
        else:
            errors.append('Please enter two identical addresses!')
    return render_to_response("newaccounts/email_change.html", {'form':form , 'errors' : errors}, context_instance=RequestContext(request))

def email_change_done(request):
	return render_to_response("newaccounts/email_change_done.html", context_instance=RequestContext(request))


def sign_out(request):
	logout(request)
	return HttpResponseRedirect("/")

#def password_change(request):
#	if request.method == 'POST':
#		password_change(request)
#	else:
#		form = PasswordChangeForm()
#	return render_to_response("password_change.html",{'form':form}, context_instance=RequestContext(request),)

def login(request):
    username = request.POST.get('username','')
    password = request.POST.get('password','')
    user = authenticate(username=username, password=password)
    if user is not None:
        if user.is_active:
            auth_login(request, user)
            return HttpResponseRedirect("/accounts/profile/" + str(username))
        else:
            html = "<html></body> Fail </body></html>"
            return HttpResponse(html)
    else:
        errors = "Username and password combination cannot be found, please try again."
        return render_to_response("newaccounts/login.html", {'errors': errors}, context_instance=RequestContext(request))


def sign_up(request):
	return render_to_response("signup.html", context_instance=RequestContext(request))

def activate_user(request, username, key):
    #remove slash from key
    key = key[:-1]
    user = User.objects.get(username = username)
    user_profile = UserProfile.objects.get(user = user)
    assert False
    if user_profile.activate_user(key):
        return HttpResponse("It worked!")
    else:
        return HttpResponse("It didnt worked!")

