from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseRedirect, JsonResponse
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required, user_passes_test
from main_app.utils import get_post_per_page, long_pagination, get_page_number_in_pagination
from main_app.models import UserExtended, Post, Category, Categorize, UserPostRelation
from .forms import EditPostForm, CreatePostForm, SignUpForm
from django.contrib.auth import views as auth_views
from .utils import *
import os, shutil
from django.conf import settings
from processors.water_mark import WaterMarker
from urllib.parse import unquote


@login_required
def home(request):
    # if request.user:
    posts = Post.objects.filter(user=request.user).order_by('-publish_date')
    # else:
    #     posts = Post.objects.order_by('-publish_date')
    
    # if request.user.is_superuser:
    #     # filtering by user
    #     # removing empty objects
    #     posts = list(filter(None, [Post.objects.filter(user=u).order_by('-publish_date') for u in User.objects.all()]))
    #     posts.append(Post.objects.filter(user=None))
    
    post_per_page = get_post_per_page(request)
    p = Paginator(posts, post_per_page)
    total_pages = p.num_pages  # or last page

    # pagination
    if request.GET.get('page'):
        try:
            page = int(request.GET.get('page'))
        except:
            page = 1

    # if direct homepage
    else:
        page = 1

    try:
        latest_posts = p.page(page)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        latest_posts = p.page(total_pages)
        page = total_pages
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        latest_posts = p.page(1)
        page = 1

    pg_iter = long_pagination(
        current_page=page,
        total_pages=total_pages,
        showing=get_page_number_in_pagination(request),  # page number showing in pagination
        is_not_mobile=not request.is_mobile
    )
    
    ctx = {  # context
        "posts": latest_posts,
        'page_iter': pg_iter,
        "current_page": page,
    }
    return render(request, 'dashboard/index.html', ctx)


@user_passes_test(lambda u: u.is_superuser)
def user_based_post(request, pk):
    # that will collect facebook cron posts
    if pk == '0':
        posts = Post.objects.filter(user=None).order_by('-publish_date')
    else:
        posts = Post.objects.filter(user=User(id=pk)).order_by('-publish_date')
    
    post_per_page = get_post_per_page(request)

    p = Paginator(posts, post_per_page)
    total_pages = p.num_pages  # or last page

    # pagination
    if request.GET.get('page'):
        try:
            page = int(request.GET.get('page'))
        except:
            page = 1

    # if direct homepage
    else:
        page = 1

    try:
        latest_posts = p.page(page)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        latest_posts = p.page(total_pages)
        page = total_pages
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        latest_posts = p.page(1)
        page = 1

    pg_iter = long_pagination(
        current_page=page,
        total_pages=total_pages,
        showing=get_page_number_in_pagination(request),  # page number showing in pagination
        is_not_mobile=not request.is_mobile
    )

    ctx = {  # context
        "posts": latest_posts,
        "user_based_post": True,
        'page_iter': pg_iter,
        "current_page": page,
    }
    return render(request, 'dashboard/index.html', ctx)


@login_required
def fav_post(request):
    u = UserExtended.objects.get(user=request.user)
    posts = [r.post for r in UserPostRelation.objects.filter(user=u)]
    
    ctx = {  # context
        "posts": posts,
        "is_fav_page": True
    }
    return render(request, 'dashboard/index.html', ctx)


def log_in(request, **kwargs):
    if request.user.is_authenticated():
        return HttpResponseRedirect('/dashboard')
    else:
        return auth_views.login(request, **kwargs)


def signup(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect('/dashboard')
    else:
        if request.method == 'POST':
            form = SignUpForm(request.POST)
            if form.is_valid():
                form.save()
                username = form.cleaned_data.get('username')
                raw_password = form.cleaned_data.get('password1')
                user = authenticate(username=username, password=raw_password)
                login(request, user)
                return redirect('/dashboard')
            else:
                print(form)
        else:
            form = SignUpForm()
        return render(request, 'dashboard/sign-up.html', {'form': form})


@login_required
def edit_post(request, pk):
    post = get_object_or_404(Post, id=pk)
    
    if request.method == 'POST':
        cat_in_post_dict = (request.POST).dict()
        print("cat_in_post_dict:  ", cat_in_post_dict, "    request: ", request.POST)
        try:
            del cat_in_post_dict['csrfmiddlewaretoken'], cat_in_post_dict["title"], cat_in_post_dict['img'], cat_in_post_dict['status'], cat_in_post_dict['nsfw']
        except:
            pass
        
        x = list(cat_in_post_dict.values())
        
        update_category(post, x, Category, Categorize)
        
        form = EditPostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save(commit=True)
            return HttpResponseRedirect('/dashboard/')
    else:
        form = EditPostForm(instance=post)
    
    ctx = {  # context
        "post": post,
        "form": form,
        "type": EDIT_OR_CREATE["edit"],
        "is_edit": True,
        "all_categories": get_category_list_by_post(Category, Categorize, post),
    }
    return render(request, "dashboard/edit-or-create-post.html", ctx)


@login_required
def delete_post(request, pk):
    post = get_object_or_404(Post, id=pk)
    if post.is_img_exists():
        shutil.rmtree(os.path.dirname(post.img.path))
    else:
        print("No img found when deleting post, awkward!!!")
    post.delete()
    return redirect('dashboard:home')


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
            
            try:
                img_path = os.path.join(settings.BASE_DIR, unquote(f.img.url.strip('/')))
                water_mark = WaterMarker(img_path, os.path.join(settings.BASE_DIR, 'media/temp/marker.png'))
                water_mark.water_mark()
            except:
                print("water mark is not successful")
                pass
            
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
    
    ctx = {  # context
        "form": form,
        "type": EDIT_OR_CREATE["create"],
        "all_categories": get_category_list_by_post(Category, Categorize),
        "category_prefix": cat_prefix
    }
    return render(request, "dashboard/edit-or-create-post.html", ctx)


@login_required
def add_category(request):  # add new category and build relation with the post
    data = {}
    if request.method == 'POST':
        new_cat_name = request.POST["new_cat"]
        # print(request.POST)
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
