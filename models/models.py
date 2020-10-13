from django.db import models
from django.contrib.auth.models import AbstractUser
from PIL import Image
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
from django.conf import settings
# from django_base64field.fields import Base64Field
ROLE = (('admin','admin'),('editor','editor'))
class User(AbstractUser):
    email = models.EmailField(unique=True)
    role = models.CharField(max_length=30,null=False,blank=False,choices=ROLE)

# class Blog(models.Model):
#     title = models.CharField(max_length=255,null=False,blank=False)
#     blog_author = models.ForeignKey(User,on_delete=models.CASCADE)

class News(models.Model):
    news_author = models.ForeignKey(User,on_delete=models.CASCADE)
    news_category = models.CharField(max_length=150,null=False,blank=False)
    news_head =  models.CharField(max_length=150,null=False,blank=False)
    news_body = models.TextField(null=False,blank=False)
    news_image = models.ImageField(null=True,blank=True)

    def set_news_author(self, news_author):
        self.news_author = news_author

    def set_news_image(self,news_image):
        self.news_image = news_image

class Contact(models.Model):
    name = models.CharField(max_length=100,null=False,blank=False)
    email = models.EmailField(max_length=100,null=False,blank=False)
    subject = models.CharField(max_length=150,null=True,blank=True)
    message = models.TextField(null=False,blank=False)

class Features(models.Model):
    name = models.CharField(max_length=100,null=False,blank=False)
    email = models.EmailField(max_length=100,null=False,blank=False)
    feature = models.CharField(max_length=150,null=False,blank=False)
    message = models.TextField(null=False,blank=False)

class DigitsSecurity(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    digits = models.CharField(max_length=10)
    creation_time = models.DateField(auto_now_add=True)

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)