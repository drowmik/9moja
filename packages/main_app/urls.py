from django.conf.urls import url
from . import views


urlpatterns = [
    
    url(r'^$', views.index, name='index'),
    
    url(r'^coming-soon/$', views.coming_soon, name='coming_soon'),
    
    url(r'^search/$', views.search, name='search'),
    
    url(r'^like_post/$', views.like_post, name='like_post'),
    
    # public page, so need a slug for better seo
    url(r'^(?P<pk>[\d]+)/(?P<slug>[-\S]+)/$', views.each_post, name='each_post'),
    
    url(r'^(?P<slug>[-\S]+)/$', views.each_category, name='each_category'),
    
]