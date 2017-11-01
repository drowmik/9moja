from django.shortcuts import render
from django.http import Http404
from .models import Post
#from core import settings


def index(request):
    latest_posts = Post.objects.order_by('-publish_date')
    
    r = request   #request
    t = 'main_app/index.html'   #template name
    c = {  #context
        "latest_posts": latest_posts
    }
    return render(r, t, c)


def each_post(request, slug):
    try:
        post = Post.objects.get(slug=slug)
    except Post.DoesNotExist:
        raise Http404("This does not exist")
    
    r = request   #request
    t = 'main_app/single_post.html'   #template name
    c = {  #context
        'post': post,
         'media_url': post.img.url
    }
    return render(r, t, c)
