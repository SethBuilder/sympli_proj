from django.shortcuts import render
from sympli.models import Article, ContentSource
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from time import sleep

def context_generator(request, title, category):
	"""made this function because views are very similar"""
	context_dict={}
	
	if(category == "index"):
		articles_list = Article.objects.order_by('-pub_date')
	else:
		articles_list = Article.objects.filter(category=category).order_by('-pub_date')

	page = request.GET.get('page', 1)
	paginator = Paginator(articles_list, 18)

	try:
		sleep(0)
		articles = paginator.page(page)
	except PageNotAnInteger:
		articles = paginator.page(1)
	except EmptyPage:
		articles = paginator.page(paginator.articles_list)

	context_dict['articles'] =  articles
	context_dict['title'] = title

	return context_dict


def index(request):
	return render(request, 'sympli/index.html', context_generator(request, "Sympli | أخباري ببساطه", "index"))

def worldnews(request):
	return render(request, 'sympli/index.html', context_generator(request, "Sympli | أخبار العالم", "world_news"))

def science_and_tech(request):
	return render(request, 'sympli/index.html', context_generator(request, "Sympli | علوم و تكنولوجيا", "science_and_tech"))

def health(request):
	return render(request, 'sympli/index.html', context_generator(request, "Sympli | صحه", "health"))

def trending(request):
	return render(request, 'sympli/index.html', context_generator(request, "Sympli | ترند", "trending"))

def travel(request):
	return render(request, 'sympli/index.html', context_generator(request,"Sympli | سياحه و سفر", "travel"))

def culture(request):
	return render(request, 'sympli/index.html', context_generator(request, "Sympli |ثقافه و فن", "culture"))

def sport(request):
	return render(request, 'sympli/index.html', context_generator(request, "Sympli |رياضه", "sport"))

def variety(request):
	return render(request, 'sympli/index.html', context_generator(request, "Sympli |منوعات", "variety"))

def show_article(request, article_id):
	context_dict={}
	article = Article.objects.get(pk = article_id)
	# get_object_or_404(MyModel, pk=1)
	print('AAAAAAAAArticle' + str(article.id))
	context_dict['article'] =  article
	return render(request, 'sympli/article.html', {'article': article})