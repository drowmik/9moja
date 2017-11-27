from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render
from django.http import Http404
from .models import Post, Category, Categorize

# multi used variables
categories = Category.objects.all()  # limited


def index(request):
    posts = Post.objects.order_by('-publish_date').filter(status="p")  # showing only published posts
    p = Paginator(posts, 10)  # show 10 post per page
    total_pages = p.num_pages
    
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
        latest_posts = p.page(p.num_pages)
        page = p.num_pages
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        latest_posts = p.page(1)
        page = 1
    
    showing_item = 5
    extra = 2
    pg_iter = long_pagination(
        current_page=page,
        total_pages=total_pages,
        showing=showing_item,
        extra=2,
        dots='...'
    )
    
    start_end = {
        "start": True if page > extra + 1 else False,  # start button appears
        "end": True if (page + extra) < total_pages else False,  # end button appears
    }
    templ = 'main_app/index.html'  # template name
    ctx = {  # context
        "posts": latest_posts,
        "categories": categories,
        "start_end": start_end,
        "page_iter": pg_iter,
        "current_page": page,
    }
    return render(request, templ, ctx)


def long_pagination(current_page, total_pages, showing, extra, dots):
    """
        prev * * a * * next
        1. Total pages <= showing: show all pages
        2. Current page + extra < total page: show next prev button
        3. Current page + extra >= total: previous pages
    """
    
    # show all pages
    if total_pages <= showing or current_page <= (extra + 1):
        page_iter = [x for x in range(1, min(total_pages + 1, showing + 1))]
        if current_page <= (extra + 1) and total_pages >= showing:
            page_iter.append(dots)
    
    # have pages before and after
    elif (current_page + extra) < total_pages:
        page_iter = [x for x in range(current_page - extra, current_page + 3)]
        page_iter.insert(0, dots)
        page_iter.append(dots)
    
    # only have pages before
    else:
        page_iter = [x for x in range(total_pages - showing - 1, total_pages + 1)]
        page_iter.insert(0, dots)
    
    return page_iter


def each_post(request, slug, pk):
    try:
        post = Post.objects.get(id=pk)
    except Post.DoesNotExist:
        raise Http404("This does not exist")
    
    templ = 'main_app/single_post.html'  # template name
    ctx = {  # context
        'post': post,
        'media_url': post.img.url
    }
    return render(request, templ, ctx)


def each_category(request, slug):
    try:
        category = Category.objects.get(slug=slug)
        
        relation = category.categorize_set.all()
        
        posts_by_category = [cp.post for cp in relation]
        
        p = Paginator(posts_by_category, 10)
    
    except Category.DoesNotExist:
        raise Http404("This type of category does not exist!")
    
    templ = 'main_app/index.html'
    ctx = {
        "is_category_template": True,
        "posts": posts_by_category,
        "categories": categories,
        "pagination": p,
    }
    return render(request, templ, ctx)


def coming_soon(request):
    return render(request, 'main_app/coming-soon.html')
