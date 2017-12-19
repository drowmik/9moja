from django.contrib import admin
from .models import FacebookAuth, FacebookData, ScrappedData, SocialAuth


@admin.register(FacebookAuth)
class FacebookAuthAdmin(admin.ModelAdmin):
    list_display = [ 'app_id', 'id']
    
    list_display_links = ['app_id']


@admin.register(FacebookData)
class FacebookDataAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'page', 'media_file_counter']
    
    list_display_links = ['id', 'name', 'page']


@admin.register(ScrappedData)
class ScrappedDataAdmin(admin.ModelAdmin):
    list_display = ['id', 'post_id', 'likes', 'shares', 'score']


@admin.register(SocialAuth)
class SocialAuthAdmin(admin.ModelAdmin):
    list_display = ['name', 'app_id', 'secret_id']
    
    list_display_links = ['name']