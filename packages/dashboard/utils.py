EDIT_OR_CREATE = {
    "edit": "edit",
    "create": "create",
    "template": "dashboard/edit-or-create-post.html"
}


# this will call only on a login required view,
# so no need to check login
def update_category(post, cat_list, category_model, categorize_model):
    cat_list = list(map(int, cat_list))  # all categories
    all_cat_list = list(category_model.objects.values_list('id', flat=True))  # categories assigned for this post
    
    for cat in all_cat_list:
        if cat in cat_list:  # check if any new category is added
            categorize_model.objects.update_or_create(
                post=post,
                category=category_model.objects.get(id=cat),
            )
        else:  # if unmarked, delete it
            obj = categorize_model.objects.filter(category=cat, post=post)  # delete only selected relation with post and category
            if obj:
                obj.delete()  # delete queryset if not changed from unassigned


def get_category_list_by_post(category_model, categorize_model, pst=None):
    cat_list = []
    
    for cat in category_model.objects.all():
        if cat.name in [x.category.name for x in categorize_model.objects.filter(post=pst)]:  # all categories of this post
            flag = True
        else:
            flag = False
        
        # all categories including a flag containing this post have this category or not
        cat_list.append({
            "has_category": flag,
            "category": cat
        })
    
    return cat_list
