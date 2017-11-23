from django.conf.urls import url
from . import views


urlpatterns = [
    
    url(r'^$', views.home, name='home'),
    
    url(r'^scrapper/$', views.scrapper, name='scrapper'),
    
    url(r'^scrapper-auth-form/$', views.get_fb_scrapper_auth, name='scrapper_auth_form'),
    
    url(r'^scrapper-data-form/$', views.get_fb_scrapper_data, name='scrapper_data_form'),
    
    url(r'^save-token/$', views.scrapper_ajax, name='scrapper_ajax'),
    
    url(r'^scrap-data/$', views.get_data_ajax, name='scrapper_data_ajax'),
    
]