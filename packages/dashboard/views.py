from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from main_app.models import Post, Category
from .forms import EditPostForm, CreatePostForm


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
    post = get_object_or_404(Post, id=pk)
    
    if request.method == 'POST':
        form = EditPostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save(commit=True)
            return HttpResponseRedirect('/dashboard/')
    else:
        form = EditPostForm(instance=post)
    
    templ = 'dashboard/edit-post.html'   #template name
    ctx = {  #context
        "post": post,
        "form": form,
        "type": "edit",
    }
    return render(request, templ, ctx)


@login_required
def create_post (request):
    
    if request.method == 'POST':
        form = CreatePostForm(request.POST, request.FILES)
        if form.is_valid():
            f = form.save(commit=False)
            f.user = request.user
            f.save()
            return HttpResponseRedirect('/dashboard/')
    else:
        form = CreatePostForm()
    
    templ = 'dashboard/edit-post.html'   #template name
    ctx = {  #context
        # "post": post,
        "form": form,
        "type": "create",
    }
    return render(request, templ, ctx)


