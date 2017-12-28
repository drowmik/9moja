from django.utils import six
from django.utils.functional import keep_lazy
from django.contrib.auth import get_user_model
from django.utils.safestring import SafeText, mark_safe
import re, unicodedata, string

User = get_user_model()

STATUS_CHOICES = (
    ('p', 'Published'),
    ('u', 'Unpublished'),
    ('a', 'Archived'),
)

social_site_font = [
    "fa fa-facebook",
    "fa fa-twitter",
    "fa fa-youtube-play",
    "fa fa-soccer-ball-o",
]


# unicode allowed
@keep_lazy(six.text_type, SafeText)
def custom_slugify(value):
    value = unicodedata.normalize('NFKC', value)
    punc = set(string.punctuation)  # set of punctuations
    v = ''.join(ch for ch in value if ch not in punc)  # remove punctuations first
    return mark_safe(re.sub(r'[-\s]+', '-', v, flags=re.U))  # slugify including different language


def long_pagination(current_page, total_pages, showing, is_not_mobile=True):
    """
        prev * * a * * next
        1. Total pages <= showing: show all pages
        2. Current page + extra < total page: show next prev button
        3. Current page + extra >= total: previous pages
    """
    
    dots = '...'
    extra = int((showing - 1) / 2)  # extra page link before and after active page,
    
    if total_pages <= showing or current_page <= (extra + 1):
        # show all pages
        page_iter = [x for x in range(1, min(total_pages + 1, showing + 1))]
        if is_not_mobile and (current_page <= (extra + 1) and total_pages >= showing):
            # show dots after pagination
            page_iter.append(dots)
    
    # have pages before and after
    elif (current_page + extra) < total_pages:
        page_iter = [x for x in range(current_page - extra, current_page + extra + 1)]
        if is_not_mobile:
            page_iter.insert(0, dots)
            page_iter.append(dots)
    
    # only have pages before
    else:
        page_iter = [x for x in range(total_pages - showing + 1, total_pages + 1)]
        if is_not_mobile:
            page_iter.insert(0, dots)
    
    return page_iter


def liking_post(user, post, relation_model, is_liked=True):
    """
    when a user click like on a post, then this action will be triggered
    """
    try:
        #if is_liked:
        r = relation_model(
            user=user,
            post=post
        )
        post.likes += 1
        user.likes += 1
        r.save()
        post.save()
        user.save()
            
            # no disliking initially... muhuhhahahahah
            # else:
            #     r = relation_model.objects.filter(
            #         user=user,
            #         post=post
            #     )
            #     r.delete()
            #     post.likes -= 1
            #     user.likes -= 1
            # user.save()
            # post.save()
    except:
        print("unexpected error!! (print from: main_app/utils.py)")
        return


def get_page_number_in_pagination(req):
    """page number showing in pagination"""
    return 3 if req.is_mobile else 5


def get_post_per_page(req):
    """post per page"""
    return 4 if req.is_mobile else 8
