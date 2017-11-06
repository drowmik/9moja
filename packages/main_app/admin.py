from django.contrib import admin
from .models import Post, Category, Categorize


def make_published(modeladmin, request, queryset):
    queryset.update(status='p')
make_published.short_description = "Make selected as Published"

def make_unpublished(modeladmin, request, queryset):
    queryset.update(status='u')
make_unpublished.short_description = "Make selected as Unpublished"

def make_archived(modeladmin, request, queryset):
    queryset.update(status='a')
make_archived.short_description = "Make selected as Archived"


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    # date_hierarchy = 'publish_date'
    list_display = ['id', 'status', 'title', 'publish_date']
    actions = [make_published, make_unpublished, make_archived]

admin.site.register(Category)

admin.site.register(Categorize)