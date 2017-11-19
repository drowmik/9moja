from django.contrib import admin
from .models import FacebookAuth, FacebookData


@admin.register(FacebookAuth)
class FacebookAuthAdmin(admin.ModelAdmin):
    list_display = [ 'app_id', 'id']
    
    list_display_links = ['app_id']


@admin.register(FacebookData)
class FacebookDataAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'page', 'media_file_counter']
    
    list_display_links = ['id', 'name', 'page']