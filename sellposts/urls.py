from django.conf.urls import patterns, url
from .views import index, render_individual_sellpost, search

urlpatterns = patterns('', 
    #homepage
    url(r'^$', index), 
    #renders individual picture page
    url(r'images/(\d+\.[A-Za-z]+)/sellpostpics', render_individual_sellpost),
    url(r'images/(.+)/sellposttures', render_individual_sellpost),
    url(r'search', search),
    )
