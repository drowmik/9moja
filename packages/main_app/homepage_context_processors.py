from .models import Category


def header(request):
    categories = Category.objects.all()
    
    dummy_pages = [
        "পুরস্কার জিতুন",  # "Get a prize",
        "জনপ্রিয় মিম",  # "Top MeMes",
        "জনপ্রিয় বিভাগ",  # "Top Categories",
        "জনপ্রিয় পোস্টদাতা",  # "Best meme-guy",
        #"লগইন",  # "login",
        "সাইন আপ",  # "sign-up",
        "এপ ব্যবহার করুন",  # "use app",
        # " যোগাযোগ করুন",#"contact",
    ]
    
    social_site_font = [
        "fa fa-facebook",
        "fa fa-twitter",
        "fa fa-youtube-play",
        "fa fa-soccer-ball-o",
    ]
    
    return {
        "hcp_categories": categories,  # showing categories in header at base.html
        "hcp_limit": 5,  # limit for showing category in header menu (other categories will be shown in a dropdown menu)
        
        "hcp_dummy_pages": dummy_pages,  # dummy pages for header menu
        "hcp_socials": social_site_font,  # social site's font awesome icon
    }
