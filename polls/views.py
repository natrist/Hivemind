# For filtering
from django.db.models import Q
# For the oopsies
from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse

from .models import Article, Category, Comment, UserProfile


def index(request):
    hot_articles = Article.objects.order_by('-date_created')[:5]
    context = {'hot_articles': hot_articles}
    print(request.user.is_authenticated)
    return render(request, 'polls/index.html', context)

def detail(request, article_id):
    try:
        article = Article.objects.get(pk=article_id)
        userprofile = UserProfile.objects.get(pk=article.author.id)
        comment = Comment.objects.get(pk=article_id)
    except Article.DoesNotExist:
        raise Http404("Article does not exist")
    except Comment.DoesNotExist:
        comment = None
    return render(request, 'polls/detail.html', {'article': article, 'userprofile':userprofile, 'comment': comment})

def search(request):
    # GET request handling
    if request.method == 'GET':
        search = request.GET.get('search', None)
        if search is None or search == "":
            return redirect("index")
    # CONTINUE
    article_results = Article.objects.filter(Q(name__icontains=search)|Q(description__icontains=search))
    comment_results = Comment.objects.filter(comment__icontains=search)
    #total_results = article_results + comment_results
    total_results = article_results.count() + comment_results.count()
    context = {'article_results': article_results, 'comment_results': comment_results, 'search': search, 'total_results': total_results}
    return render(request, 'polls/search.html', context)

def login (request):
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(user)
        return redirect(index)
