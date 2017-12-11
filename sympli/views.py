from django.shortcuts import render
from sympli.models import Article, ContentSource
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from time import sleep

def context_generator(request, title, category):
	"""made this function because views are very similar"""
	context_dict={}
	
	if(category == "الصفحه_الرئيسيه"):
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
	return render(request, 'sympli/index.html', context_generator(request, "أخباري ببساطه", "الصفحه_الرئيسيه"))

def worldnews(request):
	return render(request, 'sympli/index.html', context_generator(request, "أخبار العالم", "أخبار_العالم"))

def science_and_tech(request):
	return render(request, 'sympli/index.html', context_generator(request, "علوم و تكنولوجيا", "علوم_و_تكنولوجيا"))

def health(request):
	return render(request, 'sympli/index.html', context_generator(request, "صحه", "صحه"))

def trending(request):
	return render(request, 'sympli/index.html', context_generator(request, "ترند", "ترند"))

def travel(request):
	return render(request, 'sympli/index.html', context_generator(request,"سياحه و سفر", "سياحه_و_سفر"))

def culture(request):
	return render(request, 'sympli/index.html', context_generator(request, "ثقافه و فن", "ثقافه_و_فن"))

def sport(request):
	return render(request, 'sympli/index.html', context_generator(request, "رياضه", "رياضه"))

def variety(request):
	return render(request, 'sympli/index.html', context_generator(request, "منوعات", "منوعات"))

def show_article(request, category, article_id):
	context_dict={}
	article = Article.objects.get(pk = article_id)
	context_dict['article'] =  article
	context_dict['category'] =  category
	return render(request, 'sympli/article.html', context_dict)