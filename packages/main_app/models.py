from django.db import models
from django.utils import timezone
from django.template.defaultfilters import slugify


class Post(models.Model):
    
    slug = models.SlugField(editable=False) # hidden in admin panel
    
    title = models.CharField(max_length=200)
    
    publish_date = models.DateTimeField(default=timezone.now)

    img = models.ImageField()
    
    category = models.ManyToManyField(
        'main_app.Category',
        through='Categorize',
        through_fields=(
            'post',
            'category'
        ),
    )

    def __str__(self):
        return self.title

    # override models save method for slug saving:
    def save(self, *args, **kwargs):
        if not self.id:
            self.slug = slugify(self.title)
        super(Post, self).save()    # saving the slug automatically
        
        
class Category(models.Model):
    
    name = models.CharField(max_length=25, default='uncategorized')
    
    slug = models.SlugField(editable=False) # hidden in admin panel

    def __str__(self):
        return self.name
    
    # override models save method for slug saving:
    def save(self, *args, **kwargs):
        if not self.id:
            self.slug = slugify(self.name)
        super(Category, self).save()    # saving the slug automatically
        

class Categorize(models.Model):
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE
    )
    
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE
    )
    



