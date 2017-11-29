from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect, JsonResponse
from django.contrib.auth.decorators import login_required
from main_app.models import Post, Category, Categorize
from .forms import EditPostForm, CreatePostForm

EDIT_OR_CREATE = {
    "edit": "edit",
    "create": "create",
    "template": "dashboard/edit-or-create-post.html"
}


@login_required
def home(request):
    posts = Post.objects.order_by('-publish_date')
    
    templ = 'dashboard/index.html'  # template name
    ctx = {  # context
        "posts": posts
    }
    return render(request, templ, ctx)


@login_required
def edit_post(request, pk):
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
    
    templ = EDIT_OR_CREATE["template"]  # template name
    ctx = {  # context
        "post": post,
        "form": form,
        "type": EDIT_OR_CREATE["edit"],
        "all_categories": get_category_list_by_post(post),
    }
    return render(request, templ, ctx)


@login_required
def create_post(request):
    cat_prefix = 'cat-'
    
    if request.method == 'POST':
        form = CreatePostForm(request.POST, request.FILES)
        if form.is_valid():
            f = form.save(commit=False)
            f.user = request.user
            f.save()
            
            # should've use form.form but I don't know how to use along with model form
            # saving category when creating post
            
            # finding post by id
            # why not title?
            # if any dumb guy post same title's post it may be a pain in the ass to manage them
            # so here, I'm searching for the maximum id, which must be this form-post id
            # and get the post by id
            form_post_id = max([x.id for x in Post.objects.filter(title=request.POST['title'])])
            new_post = Post.objects.get(id=form_post_id)

            # if no category found bound on that post
            if not new_post.get_categories():
                cat, create = Category.objects.update_or_create(name="বিভাগহীন")
                Categorize.objects.update_or_create(
                    post=new_post,
                    category=cat,
                )
            [Categorize.objects.update_or_create(
                post=new_post,
                category=Category.objects.get(id=int(k[4:])),
            ) for k in request.POST if k[:4] == cat_prefix]
            return HttpResponseRedirect('/dashboard/')
    else:
        form = CreatePostForm()
    
    templ = EDIT_OR_CREATE["template"]  # template name
    ctx = {  # context
        "form": form,
        "type": EDIT_OR_CREATE["create"],
        "all_categories": get_category_list_by_post(),
        "category_prefix": cat_prefix
    }
    return render(request, templ, ctx)


def update_category(post, cat_list):
    cat_list = list(map(int, cat_list))  # all categories
    all_cat_list = list(Category.objects.values_list('id', flat=True))  # categories assigned for this post
    
    for cat in all_cat_list:
        if cat in cat_list:  # check if any new category is added
            Categorize.objects.update_or_create(
                post=post,
                category=Category.objects.get(id=cat),
            )
        else:  # if unmarked, delete it
            obj = Categorize.objects.filter(category=cat, post=post)  # delete only selected relation with post and category
            if obj:
                obj.delete()  # delete queryset if not changed from unassigned


def get_category_list_by_post(pst=None):
    cat_list = []
    
    for cat in Category.objects.all():
        if cat.name in [x.category.name for x in Categorize.objects.filter(post=pst)]:  # all categories of this post
            flag = True
        else:
            flag = False
        
        # all categories including a flag containing this post have this category or not
        cat_list.append({
            "has_category": flag,
            "category": cat
        })
    
    return cat_list


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
