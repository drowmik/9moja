from django.conf.urls import url
from . import views


urlpatterns = [
    
    url(r'^$', views.index, name='index'),
    
    # public page, so need a slug for better seo
    url(r'^(?P<pk>[\d]+)/(?P<slug>[-\w]+)/$', views.each_post, name='each_post'),
    
]