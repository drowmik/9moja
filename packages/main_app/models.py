from django.db import models
from django.utils import timezone


class Post(models.Model):
    
    post_name = models.CharField(max_length=200)
    
    publish_date = models.DateTimeField(default=timezone.now)

    post_img = models.ImageField(upload_to='media/%Y/%m/%d/')

    def __str__(self):
        return self.post_name