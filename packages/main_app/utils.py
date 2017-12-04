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

