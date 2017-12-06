from .models import Category
from .utils import dummy_pages, social_site_font


def header(request):
    categories = Category.objects.all()
    
    return {
        "hcp_categories": categories,  # showing categories in header at base.html
        "hcp_limit": 5,  # limit for showing category in header menu (other categories will be shown in a dropdown menu)
        
        "hcp_dummy_pages": dummy_pages,  # dummy pages for header menu
        "hcp_socials": social_site_font,  # social site's font awesome icon
    }
