from django.contrib import admin

from .models import Article, Category, Comment, UserProfile

# Register your models here.

class CategoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']
    ordering = ['id']
    list_display_links = list_display

class ArticleAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'date_created']
    ordering = ['id', 'name']
    list_display_links = list_display

admin.site.register(UserProfile)
admin.site.register(Article, ArticleAdmin)
admin.site.register(Comment)
admin.site.register(Category, CategoryAdmin)
