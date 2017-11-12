from django.contrib import admin
from .models import Post, Category, Categorize, STATUS_CHOICES



@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    
    # date_hierarchy = 'publish_date'

    list_display = ['id', 'title', 'status', 'publish_date']

    list_display_links = ['id', 'title']
    
    actions = ['make_published', 'make_unpublished', 'make_archived']

    def make_published(self, request, queryset):
        self.row_update_msg(request=request, queryset=queryset, status=STATUS_CHOICES[0][0], desc=STATUS_CHOICES[0][1])
    make_published.short_description = STATUS_CHOICES[0][1]
    
    def make_unpublished(self, request, queryset):
        self.row_update_msg(request=request, queryset=queryset, status=STATUS_CHOICES[1][0], desc=STATUS_CHOICES[1][1])
    make_unpublished.short_description = STATUS_CHOICES[1][1]
    
    def make_archived(self, request, queryset):
        self.row_update_msg(request=request, queryset=queryset, status=STATUS_CHOICES[2][0], desc=STATUS_CHOICES[2][1])
    make_archived.short_description = STATUS_CHOICES[2][1]

    def row_update_msg(self, request, queryset, status, desc):
        rows_updated = queryset.update(status=status)
        if rows_updated == 1:
            message_bit = "1 quote was"
        else:
            message_bit = "{0} quote were".format(rows_updated)
        self.message_user(request, "{0} {1}".format(message_bit, desc))


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    
    list_display = ['id', 'name']
    
    list_display_links = ['id', 'name']


@admin.register(Categorize)
class CategorizeAdmin(admin.ModelAdmin):
    
    list_display = ['id', 'category', 'post']
    
    list_display_links = ['id', 'category', 'post']