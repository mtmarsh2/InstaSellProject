from django.conf.urls import patterns, include, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from newaccounts.views import profile, login, email_change_done
from newaccounts.views import profile_search, sign_out, sign_up, register, user_register_success, email_change, uploadsellpostture, activate_user
from django.contrib import admin
admin.autodiscover()

urlpatterns=patterns('',
 #Below url used to redirect to proper profile using username
 url(r'profile/(\w{1,10})/$', profile, name = "profile_page"),
 (r'logout/$', sign_out),
 (r'sign_up/$', register),
 (r'login/$', login),
 (r'password_change/$', 'django.contrib.auth.views.password_change', {'template_name':'newaccounts/password_change.html'}),
 (r'password_change_done/$' ,'django.contrib.auth.views.password_change_done', {'template_name': 'newaccounts/password_change_done.html'}),
 (r'email_change/$' , email_change),
 url(r'email_change_done/$', email_change_done, name = 'email_change_done'),
 (r'profilesearch/$', profile_search),
 (r'uploadsellpostture/$', uploadsellpostture),
 url(r'register_success', user_register_success, name = 'user_register_success'),
 url(r'activate/([A-Za-z0-9]+)/(.+)$', activate_user)

)
