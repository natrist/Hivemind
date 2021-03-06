# For Quill JSON scripts
import json

# For filtering
from django.db.models import Q

# For the oopsies
from django.http import Http404, HttpResponseRedirect

from django.shortcuts import redirect, render
from django.contrib.auth import authenticate
from django.core.exceptions import ObjectDoesNotExist
from .models import Article, Comment, UserProfile


def index(request):
    hot_articles = Article.objects.order_by('-date_created')[:5]
    context = {'hot_articles': hot_articles}
    return render(request, 'polls/index.html', context)


def detail(request, article_id):
    try:
        article = Article.objects.get(pk=article_id)
        userprofile = UserProfile.objects.get(pk=article.author.id)
        comment = Comment.objects.get(pk=article_id)
    except ObjectDoesNotExist(article):
        raise Http404("Article does not exist")
    except ObjectDoesNotExist(comment):
        comment = None
    except Exception as e:
        print(e)
    if (request.method == "POST"):
        result = ""
        postContent = json.loads(request.POST["postContent"])
        for op in postContent["ops"]:
            # TODO:
            # Add attributes cases
            if "insert" in op:
                if "image" in op['insert']:
                    result += "<img src=\"{}\">".format(op['insert']['image'])
                else:
                    result += op['insert']
        newPost = Comment(article=article, comment=result, author=request.user)
        newPost.save()
    return render(
        request,
        'polls/detail.html',
        {
            'article': article,
            'userprofile': userprofile,
            'comment': comment
        }
    )


def search(request):
    # GET request handling
    if request.method == 'GET':
        search = request.GET.get('search', None)
        if search is None or search == "":
            return redirect("index")
    # CONTINUE
    article_results = Article.objects.filter(
        Q(name__icontains=search) | Q(description__icontains=search)
    )
    comment_results = Comment.objects.filter(comment__icontains=search)
    total_results = article_results.count() + comment_results.count()
    context = {
        'article_results': article_results,
        'comment_results': comment_results,
        'search': search,
        'total_results': total_results
    }
    return render(request, 'polls/search.html', context)


def login(request):
    username = request.POST['username']
    password = request.POST['password']
    authenticate(request, username=username, password=password)


def logout(request):
    logout(request)
    return HttpResponseRedirect(request.GET.get('next', '/'))


def profile(request):
    context = {}
    return render(request, 'polls/profile.html', context)
