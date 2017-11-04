from django.shortcuts import render
# from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from main_app.models import Post
# from .forms import Edit_Post_Form


@login_required
def home (request):
    posts = Post.objects.order_by('-publish_date')
    
    templ = 'dashboard/index.html'   #template name
    ctx = {  #context
        "posts": posts
    }
    return render(request, templ, ctx)


@login_required
def edit_post (request, pk):
    editable_post = Post.objects.get(id=pk)
    
    templ = 'dashboard/edit-post.html'   #template name
    ctx = {  #context
        "post": editable_post
    }
    return render(request, templ, ctx)


"""
@login_required
def edit_post_form(request):
    if request.method == 'POST':
        form = Edit_Post_Form(request.POST)
        if form.is_valid():
            return HttpResponseRedirect('/dashboard/')
    else:
        form = Edit_Post_Form()
    
    templ = 'dashboard/edit-post.html'   #template name
    ctx = {  #context
        "from": form
    }
    return render(request, templ, ctx)
"""