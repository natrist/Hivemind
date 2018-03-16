from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone


class SuperDatedModel(models.Model):
    objects = models.Manager()
    date_created = models.DateTimeField('date published')
    date_modified = models.DateTimeField('last modified')

    @property
    def is_modified(self):
        return not self.date_modified == self.date_created

    def save(self, *args, **kwargs):
        ''' On save, update timestamps '''
        if not self.date_created:
            self.date_created = timezone.now()
        self.date_modified = timezone.now()
        return super(SuperDatedModel, self).save(*args, **kwargs)

    class Meta:
        abstract = True


# UserProfile table model
class UserProfile(models.Model):
    objects = models.Manager()
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField()

    def __str__(self):
        return self.user.name


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
    objects = models.Manager()

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Categories"


# Article table model
class Article(SuperDatedModel):
    objects = models.Manager()
    name = models.CharField(max_length=255)
    description = models.TextField(max_length=3072)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Article'
        # verbose_name_plural = 'Articlos'


# Comment table model
class Comment(SuperDatedModel):
    objects = models.Manager()
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    comment = models.CharField(max_length=1024)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.comment
