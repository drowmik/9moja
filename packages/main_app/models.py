from django.db import models
from django.utils import timezone
from django.urls import reverse
from django.db.models.signals import post_save
from .utils import *
import os, datetime


# post model function
def get_image_path(instance, filename):
    file_extension = os.path.splitext(filename)[1]
    
    # the format will be /path/to/media/<post_id>/<upload_date>/<post_title><file_extension>
    return os.path.join(
        datetime.datetime.now().strftime("%Y-%m-%d"),
        str(instance.id),
        str(instance.title + file_extension)
    )


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
    
    img = models.ImageField(
        upload_to=get_image_path,
        blank=True,
        null=True
    )
    
    nsfw = models.BooleanField(default=False)
    
    def __str__(self):
        return self.title
    
    # override models save method for slug saving:
    def save(self, user=None, *args, **kwargs):
        if not self.id:
            self.slug = custom_slugify(value=self.title)
            
            backup_img = self.img
            self.img = None
            super(Post, self).save()    # saving post without img field
            self.img = backup_img
        
        if user:
            self.user = user
        super(Post, self).save()  # saving the post finally
    
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
    
    def is_img_exists(self):
        return os.path.isfile(self.img.path)


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


class UserExtended(models.Model):
    user = models.ForeignKey(
        User,
        unique=True,
        on_delete=models.CASCADE
    )
    
    likes = models.IntegerField(default=0)
    
    shares = models.IntegerField(default=0)
    
    uploads = models.IntegerField(default=0)
    
    liked_post = models.ManyToManyField(
        'main_app.Post',
        through='UserPostRelation',
        through_fields=(
            'user',
            'post',
        ),
    )
    
    def __str__(self):
        return self.user.username
    
    def get_liked_post(self):
        """
        :return: list of liked post
        """
        return [x.post for x in self.userpostrelation_set.all()]


# UserExtended function
def create_user_profile(sender, instance, created, **kwargs):
    """
    Creating Instance of UserExtended when a new user Created
    Should be used in signals
    But not working
    I left it for later use
    """
    if created:
        UserExtended.objects.create(user=instance)


post_save.connect(create_user_profile, sender=User)  # UserExtended function end


class UserPostRelation(models.Model):
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE
    )
    
    user = models.ForeignKey(
        UserExtended,
        on_delete=models.CASCADE
    )
    
    def __str__(self):
        data = {'user': self.user, 'post': self.post}
        return "{user} : {post}".format(**data)
