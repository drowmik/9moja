from django.db import models
from django.utils import timezone
from django.template.defaultfilters import slugify


class Post(models.Model):
    
    slug = models.SlugField(editable=False) # hide from admin
    
    title = models.CharField(max_length=200)

    id = models.AutoField(primary_key=True)
    
    publish_date = models.DateTimeField(default=timezone.now)

    img = models.ImageField()

    def __str__(self):
        return self.title

    # override models save method:
    def save(self, *args, **kwargs):
        if not self.id:
            self.slug = slugify(self.title)
        super(Post, self).save()