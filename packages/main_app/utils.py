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


# unicode allowed
@keep_lazy(six.text_type, SafeText)
def custom_slugify(value):
    value = unicodedata.normalize('NFKC', value)
    punc = set(string.punctuation)  # set of punctuations
    v = ''.join(ch for ch in value if ch not in punc)  # remove punctuations first
    return mark_safe(re.sub(r'[-\s]+', '-', v, flags=re.U))  # slugify including different language


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

