from django.shortcuts import render
from sympli.models import Article, ContentSource

def index(request):
	context_dict = {}

	articles = Article.objects.order_by('-pub_date')
	context_dict['articles'] =  articles
	context_dict['title'] = "Sympli | أخبارك ببساطه"
	
	return render(request, 'sympli/index.html', context_dict)


def worldnews(request):
	context_dict = {}

	articles = Article.objects.filter(category='world_news').order_by('-pub_date')
	context_dict['articles'] =  articles
	context_dict['title'] = "Sympli | أخبار العالم"
	return render(request, 'sympli/index.html', context_dict)

def science_and_tech(request):
	context_dict = {}

	articles = Article.objects.filter(category='science_and_tech').order_by('-pub_date')
	context_dict['articles'] =  articles
	context_dict['title'] = "Sympli | علوم و تكنولوجيا"
	return render(request, 'sympli/index.html', context_dict)

def health(request):
	context_dict = {}

	articles = Article.objects.filter(category='health').order_by('-pub_date')
	context_dict['articles'] =  articles
	context_dict['title'] = "Sympli | صحه"
	return render(request, 'sympli/index.html', context_dict)

def trending(request):
	context_dict = {}

	articles = Article.objects.filter(category='trending').order_by('-pub_date')
	context_dict['articles'] =  articles
	context_dict['title'] = "Sympli | ترند"
	return render(request, 'sympli/index.html', context_dict)

def travel(request):
	context_dict = {}

	articles = Article.objects.filter(category='travel').order_by('-pub_date')
	context_dict['articles'] =  articles
	context_dict['title'] = "Sympli | سياحه و سفر"
	return render(request, 'sympli/index.html', context_dict)

def culture(request):
	context_dict = {}

	articles = Article.objects.filter(category='culture').order_by('-pub_date')
	context_dict['articles'] =  articles
	context_dict['title'] = "Sympli |ثقافه و فن"
	return render(request, 'sympli/index.html', context_dict)
