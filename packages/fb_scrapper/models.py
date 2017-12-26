from django.db import models


class FacebookAuth(models.Model):
    token = models.CharField(
        max_length=300,
        blank=True,
        null=True
    )  # long term token
    
    app_id = models.CharField(max_length=20)  # generally app id length 15
    
    app_secret_id = models.CharField(max_length=64)  # generally 32
    
    def __str__(self):
        return str(self.id)


# this has been created for later usage... admin can add pages for scrapping (cron)
class FacebookData(models.Model):
    page = models.CharField(max_length=50)  # page (get from url)
    
    # page name
    name = models.CharField(
        max_length=50,
        null=True,
        blank=True,
    )
    
    # items scrapped from facebook (4 digit number)
    media_file_counter = models.CharField(
        max_length=4,
        null=True,
        blank=True,
    )
    
    def __str__(self):
        return self.page


class ScrappedData(models.Model):
    # facebook post id
    post_id = models.CharField(
        max_length=50,
        unique=True,
    )
    
    likes = models.IntegerField()
    
    shares = models.IntegerField()
    
    score = models.IntegerField()


class SocialAuth(models.Model):
    name = models.CharField(
        max_length=20,
        unique=True,
    )
    
    app_id = models.CharField(
        max_length=50,
    )
    
    secret_id = models.CharField(
        max_length=100,
    )
    
    def __str__(self):
        return str(self.name)