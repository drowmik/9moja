from django.conf.urls import url
from . import views


urlpatterns = [
    
    url(r'^$', views.home, name='home'),
    
    # url(r'^edit/(?P<pk>[\d]+)/$', views.edit_post, name='edit_post'),
    #
    # url(r'^create/$', views.create_post, name='create_post'),
    #
    # url(r'^new-category/$', views.add_category, name='add_category'),
    
]