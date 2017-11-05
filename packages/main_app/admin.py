from django.contrib import admin
from .models import Post, Category, Categorize


# Registering models
admin.site.register(Post)

admin.site.register(Category)

admin.site.register(Categorize)