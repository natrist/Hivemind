from django.contrib import admin

from .models import Article, Category, Comment, UserProfile

# Register your models here.

class SuperDatedAdmin(admin.ModelAdmin):
    readonly_fields = [
        'date_created',
        'date_modified'
    ]

class CategoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']
    ordering = ['id']
    list_display_links = list_display

class ArticleAdmin(SuperDatedAdmin):
    list_display = ['id', 'name', 'date_created']
    ordering = ['id', 'name']
    list_display_links = list_display
    # fields = []
    # fieldsets = []

admin.site.register(UserProfile)
admin.site.register(Article, ArticleAdmin)
admin.site.register(Comment)
admin.site.register(Category, CategoryAdmin)
