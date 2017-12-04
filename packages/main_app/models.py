from django.db import models
from django.utils import timezone
from django.urls import reverse
from django.db.models.signals import post_save
from .utils import *


class UserActivity(models.Model):
    user = models.ForeignKey(
        User,
        unique=True,
        on_delete=models.CASCADE
    )
    
    likes = models.IntegerField(default=0)
    
    shares = models.IntegerField(default=0)
    
    uploads = models.IntegerField(default=0)
    
    def __str__(self):
        return self.user.username


def create_user_profile(sender, instance, created, **kwargs):
    """
    Creating Instance of UserActivity when a new user Created
    Should be used in signals
    But not working
    I left it for later use
    """
    if created:
        UserActivity.objects.create(user=instance)


post_save.connect(create_user_profile, sender=User)


class Post(models.Model):
    user = models.ForeignKey(
        User,
        blank=True,
        null=True,
        on_delete=models.SET_NULL
    )
    
    slug = models.SlugField(
        allow_unicode=True,
        editable=False
    )
    
    title = models.CharField(max_length=200)
    
    likes = models.IntegerField(default=0)
    
    shares = models.IntegerField(default=0)
    
    publish_date = models.DateTimeField(default=timezone.now)
    
    status = models.CharField(
        max_length=1,
        choices=STATUS_CHOICES,
        default='u'
    )
    
    img = models.ImageField(upload_to="%Y-%m-%d")
    
    def __str__(self):
        return self.title
    
    # override models save method for slug saving:
    def save(self, user=None, *args, **kwargs):
        if not self.id:
            self.slug = custom_slugify(value=self.title)
        if user:
            self.user = user
        super(Post, self).save()  # saving the slug automatically
    
    def get_categories(self):
        return self.categorize_set.all()
    
    def get_absolute_url(self):
        return reverse(
            'main_app:each_post',
            args=[
                str(self.id),
                str(self.slug)
            ]
        )


class Category(models.Model):
    name = models.CharField(max_length=25)
    
    slug = models.SlugField(
        allow_unicode=True,
        editable=False
    )
    
    post = models.ManyToManyField(
        'main_app.Post',
        through='Categorize',
        through_fields=(
            'category',
            'post',
        ),
    )
    
    def __str__(self):
        return self.name
    
    # override models save method for slug saving:
    def save(self, *args, **kwargs):
        if not self.id:
            self.slug = custom_slugify(value=self.name)
        super(Category, self).save()  # saving the slug automatically
    
    def get_absolute_url(self):
        return reverse(
            'main_app:each_category',
            args=[
                str(self.slug)
            ]
        )


class Categorize(models.Model):
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE
    )
    
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE
    )
    
    def __str__(self):
        data = {'category': self.category, 'post': self.post}
        return "{category} : {post}".format(**data)
