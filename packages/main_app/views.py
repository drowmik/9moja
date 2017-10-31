from django.shortcuts import render
from .models import Post


def index(request):
    latest_posts = Post.objects.order_by('-publish_date')
    #output = ', '.join([p.post_name for p in latest_posts])
    
    r = request   #request
    t = 'main_app/index.html'   #template name
    c = {  #context
        "latest_posts": latest_posts
    }
    return render(r, t, c)