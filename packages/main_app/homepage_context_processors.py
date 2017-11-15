from .models import Category


def header(request):
    
    categories = Category.objects.all()
    
    return {
        "categories" : categories,  # showing categories in header at base.html
    }