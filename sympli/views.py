from django.shortcuts import render
from sympli.models import Article, ContentSource
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from time import sleep

def context_generator(request, title, category):
	"""made this function because views are very similar"""
	context_dict={}
	
	if(category == "home"):
		articles_list = Article.objects.order_by('-pub_date')
	else:
		articles_list = Article.objects.filter(category=category).order_by('-pub_date')

	page = request.GET.get('page', 1)
	paginator = Paginator(articles_list, 21)

	try:
		# sleep(5)
		articles = paginator.page(page)
	except PageNotAnInteger:
		articles = paginator.page(1)
	except EmptyPage:
		articles = paginator.page(paginator.articles_list)

	context_dict['articles'] =  articles
	context_dict['title'] = title
	context_dict['category'] = category

	return context_dict


def index(request):
	return render(request, 'sympli/index.html', context_generator(request, "Home", "home"))

def world(request):
	return render(request, 'sympli/index.html', context_generator(request, "World", "world"))

def tech(request):
	return render(request, 'sympli/index.html', context_generator(request, "Tech", "tech"))

def health(request):
	return render(request, 'sympli/index.html', context_generator(request, "Health", "health"))

def trending(request):
	return render(request, 'sympli/index.html', context_generator(request, "Trend", "trend"))

def travel(request):
	return render(request, 'sympli/index.html', context_generator(request,"Travel", "travel"))

def culture(request):
	return render(request, 'sympli/index.html', context_generator(request, "Culture", "culture"))

def sport(request):
	return render(request, 'sympli/index.html', context_generator(request, "Sport", "sport"))

def us(request):
	return render(request, 'sympli/index.html', context_generator(request, "US", "us"))

def variety(request):
	return render(request, 'sympli/index.html', context_generator(request, "Variety", "variety"))

def show_article(request, category, article_id):
	context_dict={}
	article = Article.objects.get(pk = article_id)
	context_dict['article'] =  article
	context_dict['category'] =  category
	return render(request, 'sympli/article.html', context_dict)