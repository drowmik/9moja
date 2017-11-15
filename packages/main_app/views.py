from django.shortcuts import render
from django.http import Http404
from .models import Post, Category, Categorize


def index(request):
    latest_posts = Post.objects.order_by('-publish_date').filter(status="p")    # showing only published posts
    
    templ = 'main_app/index.html'   #template name
    ctx = {  #context
        "posts" : latest_posts
    }
    return render(request, templ, ctx)


def each_post(request, slug, pk):
    try:
        post = Post.objects.get(id=pk)
    except Post.DoesNotExist:
        raise Http404("This does not exist")
    
    templ = 'main_app/single_post.html'   #template name
    ctx = {  #context
        'post': post,
        'media_url': post.img.url
    }
    return render(request, templ, ctx)


def each_category(request, slug):
    try:
        category = Category.objects.get(slug=slug)
        
        posts_by_category = Categorize.objects.filter(category=category)
        
    except Category.DoesNotExist:
        raise Http404("This type of category does not exist!")
    
    templ = 'main_app/index.html'
    ctx = {
        "posts" : posts_by_category
    }
    return render(request, templ, ctx)

