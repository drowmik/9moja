"""core URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from django.conf.urls.static import static
from core import settings
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from dashboard import views as dash_views
from main_app import views as main_views
from django.contrib.auth import views as auth_views
from django.views.generic import TemplateView
from django.contrib.sitemaps.views import sitemap
import main_app.sitemap

sitemaps = {
    'single_post': main_app.sitemap.MainSitemap,
    'category': main_app.sitemap.CategorySitemap,
    'others': main_app.sitemap.OtherSitemap,
}

urlpatterns = [
    
    url(r'^dashboard/', include('dashboard.urls', namespace="dashboard")),
    
    url(r'^fbs/', include('fb_scrapper.urls', namespace="fbs")),
    
    url(r'^admin/', admin.site.urls),

    url(r'^sign-up/$', dash_views.signup, name='signup'),

    url(r'^terms/$', main_views.terms, name='terms'),

    url(r'^login/$', dash_views.log_in, {'template_name': 'dashboard/login.html'}, name='login'),
    
    # default auth logout, redirect to main page
    url(r'^logout/$', auth_views.logout, {'next_page': '/'}, name='logout'),
    
    url(r'^oauth/', include('social_django.urls', namespace='social')),
    
    url(r'^comments/', include('django_comments.urls')),
    
    url(r'^sitemap\.xml$', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),
    
    url(r'^robots.txt$', TemplateView.as_view(template_name="robots.txt", content_type="text/plain"), name="robots_file"),
    
    url(r'^', include('main_app.urls', namespace="main_app")),
    
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += staticfiles_urlpatterns()
