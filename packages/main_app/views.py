from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render, redirect
from django.db.models import Sum
from django.http import Http404
from .models import Post, Category, UserExtended, UserPostRelation
from .utils import *
from django.http import JsonResponse

# multi used variables
categories = Category.objects.all()  # limited
popular_posts = Post.objects.order_by('-likes')
popular_cats = Category.objects.filter(post__likes__isnull=False).annotate(like_count=Sum('post__likes')).order_by('-like_count')


def index(request):
    posts = Post.objects.order_by('-publish_date').filter(status="p")  # showing only published posts
    
    if request.is_mobile:
        pagination_item = 3 # page number showing in pagination
        post_per_page = 1
    else:
        pagination_item = 5 # page number showing in pagination
        post_per_page = 5
    
    p = Paginator(posts, post_per_page)
    total_pages = p.num_pages  # or last page
    
    # pagination
    if request.GET.get('page'):
        page = int(request.GET.get('page'))
    
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
    
    if request.user.is_authenticated():
        """
        if logged in user
        liked post will be marked in homepage
        """
        user = UserExtended.objects.get(user=request.user)
        for p in latest_posts:
            try:
                p.have_like = "1" if UserPostRelation.objects.get(user=user, post=p) else "0"
            except:
                p.have_like = "0"
    
    pg_iter = long_pagination(
        current_page=page,
        total_pages=total_pages,
        showing=pagination_item,    # page number showing in pagination
        is_not_mobile=not request.is_mobile
    )
    
    templ = 'main_app/index.html'  # template name
    ctx = {  # context
        "posts": latest_posts,
        "popular_posts": popular_posts[:5],
        "popular_cats": popular_cats[:5],
        "page_iter": pg_iter,
        "current_page": page,
    }
    return render(request, templ, ctx)


def each_post(request, slug, pk):
    share_urls = {}
    try:
        post = Post.objects.get(id=pk)
        
        full_url = str(request.scheme) + "://" + str(request.get_host()) + str(post.get_absolute_url())
        
        share_urls["fb"] = "https://www.facebook.com/plugins/share_button.php?href=" + \
                           full_url + \
                           "&layout=button_count&size=small&mobile_iframe=true&width=70&height=30&appId"
        share_urls["twt"] = "http://twitter.com/share?text=visit www.9moja.com for more&url=" + \
                            full_url + "&hashtags=মজা,নয়মজা,ফানি,9moja,funny,meme,bangla_meme"
        share_urls["gp"] = "https://plus.google.com/share?url=" + full_url
    
    except Post.DoesNotExist:
        raise Http404("This does not exist")
    
    templ = 'main_app/single_post.html'  # template name
    ctx = {  # context
        'post': post,
        'media_url': post.img.url,
        'share_urls': share_urls,
    }
    return render(request, templ, ctx)


def each_category(request, slug):
    try:
        category = Category.objects.get(slug=slug)
        
        relation = category.categorize_set.all()
        
        posts_by_category = [cp.post for cp in relation]
        
        p = Paginator(posts_by_category, 10)
    
    except Category.DoesNotExist:
        raise Http404(" দুঃখিত, এই নামের বিভাগ খুঁজে পাওয়া যায় নি!")
    
    templ = 'main_app/index.html'
    ctx = {
        "is_category_template": True,
        "posts": posts_by_category,
        "popular_posts": popular_posts[:5],
        "popular_cats": popular_cats[:5],
        "pagination": p,
    }
    return render(request, templ, ctx)


def coming_soon(request):
    return render(request, 'main_app/coming-soon.html')


def search(request):
    result = None
    err = None
    if request.method == 'GET':
        keyword = request.GET.get('q')  # search keyword
        
        if keyword:
            posts = Post.objects.filter(title__contains=keyword)  # post
            cats = Category.objects.filter(name__contains=keyword)  # categories
            result = {
                "posts": posts,
                "cats": cats
            }
            err = None if posts or cats else "No result"
        else:
            # if no search keyword found, redirect to homepage
            return redirect('/')
    
    templ = 'main_app/search.html'
    ctx = {
        "result": result,
        "err": err
    }
    return render(request, templ, ctx)


def like_post(request):
    if request.method == 'GET':
        ajax_data = request.GET
        pk = ajax_data.get("post_id")
        jd = {}
        
        post = Post.objects.get(id=pk)
        user = UserExtended.objects.get(user=request.user)
        if ajax_data.get("is_liked") == "1":
            # dislike
            liking_post(user, post, UserPostRelation, False)
            jd["is_liked"] = "0"
        elif ajax_data.get("is_liked") == "0":
            # like
            liking_post(user, post, UserPostRelation, True)
            jd["is_liked"] = "1"
        else:
            # empty response
            # old value won't change
            jd["is_liked"] = ajax_data.get("is_liked")
            return JsonResponse(jd)
        
        # jd["likes"] = post.likes
        
        print(jd)
        
        return JsonResponse(jd)
    
    return JsonResponse({
        "error": {
            "message": "Unexpected Error"
        }
    })


def popular_categories(request):
    return each_category(request, popular_cats[0].slug)


def best_meme(request):
    return each_post(request, popular_posts[0].slug, popular_posts[0].id)
