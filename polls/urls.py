from django.urls import path

from . import views

urlpatterns = [
    # ex: /polls/
    path('', views.index, name='index'),
    # ex: /polls/5/
    path('post/<int:article_id>/', views.detail, name='detail'),
    #path("^search/<string:search_q>/$", views.search, name="search")
    path("search/", views.search, name="search")
]
