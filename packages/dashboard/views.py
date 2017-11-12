from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from main_app.models import Post, Category, Categorize
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
        cat_in_post_dict = (request.POST).dict()
        del cat_in_post_dict['csrfmiddlewaretoken'], cat_in_post_dict["title"], cat_in_post_dict['img']
    
        x = list(cat_in_post_dict.values())
        
        update_category(post, x)
        
        form = EditPostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save(commit=True)
            return HttpResponseRedirect('/dashboard/')
    else:
        form = EditPostForm(instance=post)
    
    cat_list = []
    
    for cat in Category.objects.all():
        if cat.name in [x.category.name for x in Categorize.objects.filter(post=post)]:     # all categories of this post
            flag = True
        else:
            flag = False

        # all categories including a flag containing this post have this category or not
        cat_list.append({
            "has_category":flag,
            "category" : cat
        })
    
    templ = 'dashboard/edit-post.html'   #template name
    ctx = {  #context
        "post": post,
        "form": form,
        "type": "edit",
        "all_categories" : cat_list,
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

def update_category ( post, cat_list ):

    cat_list = list(map(int, cat_list))     # all categories
    all_cat_list = list(Category.objects.values_list('id', flat=True))      # categories assigned for this post

    for cat in all_cat_list:
        if cat in cat_list:
            Categorize.objects.update_or_create(
                post=post,
                category= Category.objects.get(id=cat),
            )
        else:
            obj = Categorize.objects.select_related().filter(category=cat)
            if obj:
                obj.delete()    # delete queryset if not changed from unassigned