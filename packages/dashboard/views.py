from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect, JsonResponse
from django.contrib.auth.decorators import login_required
from main_app.models import UserExtended, Post, Category, Categorize
from .forms import EditPostForm, CreatePostForm
from django.contrib.auth import views as auth_views
from .utils import *


@login_required
def home(request):
    if request.user:
        posts = Post.objects.filter(user=request.user).order_by('-publish_date')
    else:
        posts = Post.objects.order_by('-publish_date')
    
    templ = 'dashboard/index.html'  # template name
    ctx = {  # context
        "posts": posts
    }
    return render(request, templ, ctx)


def login(request, **kwargs):
    if request.user.is_authenticated():
        return HttpResponseRedirect('/dashboard')
    else:
        return auth_views.login(request, **kwargs)


@login_required
def edit_post(request, pk):
    post = get_object_or_404(Post, id=pk)
    
    if request.method == 'POST':
        cat_in_post_dict = (request.POST).dict()
        del cat_in_post_dict['csrfmiddlewaretoken'], cat_in_post_dict["title"], cat_in_post_dict['img']
        
        x = list(cat_in_post_dict.values())
        
        update_category(post, x, Category, Categorize)
        
        form = EditPostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save(commit=True)
            return HttpResponseRedirect('/dashboard/')
    else:
        form = EditPostForm(instance=post)
    
    templ = EDIT_OR_CREATE["template"]  # template name
    ctx = {  # context
        "post": post,
        "form": form,
        "type": EDIT_OR_CREATE["edit"],
        "all_categories": get_category_list_by_post(Category, Categorize, post),
    }
    return render(request, templ, ctx)


@login_required
def create_post(request):
    cat_prefix = 'cat-'
    
    if request.method == 'POST':
        form = CreatePostForm(request.POST, request.FILES)
        if form.is_valid():
            f = form.save(commit=False)
            
            user = request.user
            f.user = user
            f.save()  # saving post
            
            upload_post(UserExtended, user)
            
            # should've use form.form but I don't know how to use along with model form
            # saving category when creating post
            
            # finding post by id
            # why not title?
            # if any dumb guy post same title's post it may be a pain in the ass to manage them
            # so here, I'm searching for the maximum id, which must be this form-post id
            # and get the post by id
            form_post_id = max([x.id for x in Post.objects.filter(title=form.cleaned_data['title'])])
            new_post = Post.objects.get(id=form_post_id)
            
            # if no category found bound on that post
            is_cat = False
            for x in request.POST:
                if x[:4] == cat_prefix:
                    is_cat = True
                    continue
            
            if is_cat:
                [Categorize.objects.update_or_create(
                    post=new_post,
                    category=Category.objects.get(id=int(k[4:])),
                ) for k in request.POST if k[:4] == cat_prefix]
            else:
                cat, create = Category.objects.get_or_create(name="বিভাগহীন")
                Categorize.objects.update_or_create(
                    post=new_post,
                    category=cat,
                )
            
            return HttpResponseRedirect('/dashboard/')
    else:
        form = CreatePostForm()
    
    templ = EDIT_OR_CREATE["template"]  # template name
    ctx = {  # context
        "form": form,
        "type": EDIT_OR_CREATE["create"],
        "all_categories": get_category_list_by_post(Category, Categorize),
        "category_prefix": cat_prefix
    }
    return render(request, templ, ctx)


@login_required
def add_category(request):  # add new category and build relation with the post
    data = {}
    if request.method == 'POST':
        new_cat_name = request.POST["new_cat"]
        print(request.POST)
        # check if duplicate category
        all_cat_name = list(Category.objects.values_list('name', flat=True))
        if new_cat_name in all_cat_name:
            data["err"] = "Duplicate category not allowed"
            return JsonResponse(data)
        
        new_cat, created = Category.objects.update_or_create(  # new category created
            name=new_cat_name
        )
        
        # connect category to post only if editing
        if request.POST['type'] is EDIT_OR_CREATE["edit"]:
            post_id = int(request.POST['post_id'])
            post = Post.objects.get(id=post_id)  # find post by id
            
            # connecting post and category
            Categorize.objects.update_or_create(
                post=post,
                category=Category.objects.get(id=new_cat.id),
            )
        
        data["name"] = new_cat.name
        data["id"] = new_cat.id
    return JsonResponse(data)
