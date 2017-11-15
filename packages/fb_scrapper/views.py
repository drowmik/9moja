from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from main_app.models import Post, Category, Categorize

# https://graph.facebook.com/v2.6/oyvai/posts/?fields=full_picture&limit=20&access_token=


@login_required
def home(request):
    posts = Post.objects.order_by('-publish_date')
    
    templ = 'fb_scrapper/index.html'  # template name
    ctx = {  # context
        "posts": posts
    }
    return render(request, templ, ctx)




