from django.urls import path

from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.index, name='index'),
    path('post/<int:article_id>/', views.detail, name='detail'),
    path("search/", views.search, name="search"),
    path("login/", auth_views.login, name="login"),
    path("logout/", auth_views.logout),
    path("profile/", views.profile, name="profile")
]
