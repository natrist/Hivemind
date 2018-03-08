import datetime

from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone


# UserProfile table model
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField()

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.userprofile.save()


# Category table model
class Category(models.Model):
    name = models.CharField(max_length=255)
    class Meta:
        verbose_name_plural="Categories"

# Article table model
class Article(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(max_length=3072)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    date_created = models.DateTimeField('date published')
    date_modified = models.DateTimeField('last modified')
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

# Comment table model
class Comment(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    comment = models.CharField(max_length=1024)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    date_created = models.DateTimeField('date published')
    date_modified = models.DateTimeField('last modified')
