#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sympli_proj.settings')
import django
django.setup()

import feedparser
from sympli.models import ContentSource, Article
import dateutil.parser

def pull_xml(rss_link):
	news_feed = feedparser.parse(rss_link)
	return news_feed

def content_sources():
	rss_links = ['http://feeds.bbci.co.uk/arabic/scienceandtech/rss.xml','http://feeds.bbci.co.uk/arabic/world/rss.xml', 
	'https://www.alhurra.com/api/z-gvev_qt','https://www.alarabiya.net/.mrss/ar/medicine-and-health.xml',
	'https://www.alarabiya.net/.mrss/ar/sport.xml', 'http://feeds.bbci.co.uk/arabic/trending/rss.xml', 
	'https://www.alarabiya.net/.mrss/ar/aswaq/travel-and-tourism.xml', 'https://www.alarabiya.net/.mrss/ar/culture-and-art.xml']
	return rss_links

#GLOBAL VARIABLE
rss_links = content_sources()

def populate_content_sources():

	content_sources = []

	for rss_link in rss_links:
		feed = pull_xml(rss_link)
		content_source = ContentSource.objects.get_or_create(link = rss_link)[0]
		content_source.title = feed['channel']['title']
		content_source.description = feed['channel']['description']
		

		if content_source.link == 'https://www.alarabiya.net/.mrss/ar/sport.xml' or content_source.link == 'https://www.alarabiya.net/.mrss/ar/medicine-and-health.xml' \
		or content_source.link == 'https://www.alarabiya.net/.mrss/ar/aswaq/travel-and-tourism.xml' \
		or content_source.link == 'https://www.alarabiya.net/.mrss/ar/culture-and-art.xml':
			content_source.logo_link = 'http://cdn.presstv.com/photo/20160525/568498bd-cd4d-4e82-9cb6-30cfc749f45d.jpg' 
			content_source.logo_title = feed['channel']['title']
		else:
			content_source.logo_link = feed['channel']['image']['url']
			content_source.logo_title = feed['channel']['image']['title']

		content_source.save()

		content_sources.append(content_source)

	return content_sources

#GLOBAL VARIABLE
content_sources = populate_content_sources()




def populate_articles_bbc_science_and_tech():
	
	rss_link = rss_links[0]
	content_source = content_sources[0]
	feed = pull_xml(rss_link)

	for entry in feed.entries:
		
		article = Article.objects.get_or_create(title=entry['title'])[0]
		article.category = 'science_and_tech'
		# print(str(article.title))
		if entry['description']:
			article.description = entry['description']
		else:
			article.description = entry['summary']['summary_detail']['value']

		article.article_link = entry['link']
		article.content_source = content_source

		if 'source' in entry:
			print("BBC source")
			article.thumbnail_link = entry['source']['href']
			article.thumbnail_desc = entry['source']['title']
			
		elif 'media_thumbnail' in entry:
			print("BBC media")
			article.thumbnail_link = entry['media_thumbnail'][0]['url']
			pub_date = dateutil.parser.parse(entry['published'])
			article.pub_date = pub_date

			if entry['summary_detail']['value']:
				article.thumbnail_desc = entry['summary_detail']['value']
			else:
				article.thumbnail_desc = ['media_thumbnail'][0]['title']

		elif 'summary_detail' in entry:
			print("BBC thumbnail")
			# article.thumbnail_link = entry['thumbnail']
			article.thumbnail_desc = entry['summary_detail']['value']
			
		article.save()



def populate_articles_bbc_world_news():
	
	rss_link = rss_links[1]
	content_source = content_sources[1]
	feed = pull_xml(rss_link)

	for entry in feed.entries:
		
		article = Article.objects.get_or_create(title=entry['title'])[0]
		article.category = 'world_news'
		# print(str(article.title))
		if entry['description']:
			article.description = entry['description']
		else:
			article.description = entry['summary']['summary_detail']['value']

		article.article_link = entry['link']
		article.content_source = content_source

		if 'source' in entry:
			print("BBC source")
			article.thumbnail_link = entry['source']['href']
			article.thumbnail_desc = entry['source']['title']
			
		elif 'media_thumbnail' in entry:
			print("BBC media")
			article.thumbnail_link = entry['media_thumbnail'][0]['url']
			pub_date = dateutil.parser.parse(entry['published'])
			article.pub_date = pub_date

			if entry['summary_detail']['value']:
				article.thumbnail_desc = entry['summary_detail']['value']
			else:
				article.thumbnail_desc = ['media_thumbnail'][0]['title']

		elif 'summary_detail' in entry:
			print("BBC thumbnail")
			# article.thumbnail_link = entry['thumbnail']
			article.thumbnail_desc = entry['summary_detail']['value']
			
		article.save()



def populate_articles_alhurra_tech():
	
	rss_link = rss_links[2]
	content_source = content_sources[2]
	feed = pull_xml(rss_link)
	
	for entry in feed.entries:
		
		article = Article.objects.get_or_create(title=entry['title'])[0]
		article.category = 'science_and_tech'
		# print(str(article.title))
		if entry['description']:
			article.description = entry['description']
		else:
			article.description = entry['summary']['summary_detail']['value']

		article.article_link = entry['link']
		article.content_source = content_source

		if 'source' in entry:
			print("hurra source")
			article.thumbnail_link = entry['source']['href']
			article.thumbnail_desc = entry['source']['title']
			
		elif 'media_thumbnail' in entry:
			print("hurra media")
			article.thumbnail_link = entry['media_thumbnail'][0]['url']
			pub_date = dateutil.parser.parse(entry['published'])
			article.pub_date = pub_date

			if entry['summary_detail']['value']:
				article.thumbnail_desc = entry['summary_detail']['value']
			else:
				article.thumbnail_desc = ['media_thumbnail'][0]['title']

		elif 'summary_detail' in entry:
			print("hurra thumbnail")
			# article.thumbnail_link = entry['thumbnail']
			article.thumbnail_desc = entry['summary_detail']['value']
			# print(str(entry['links']))
			article.thumbnail_link = entry['links'][1]['href']
			pub_date = dateutil.parser.parse(entry['published'])
			article.pub_date = pub_date
			
		article.save()






def populate_articles_arabiya_health():
	
	rss_link = rss_links[3]
	content_source = content_sources[3]
	feed = pull_xml(rss_link)
	print(feed.entries)
	for entry in feed.entries:
		
		article = Article.objects.get_or_create(title=entry['title'])[0]
		article.category = 'health'
		# print(str(article.title))
		if entry['description']:
			article.description = entry['description']
		else:
			article.description = entry['title']

		article.article_link = entry['link']
		article.content_source = content_source

		if 'source' in entry:
			print("arabiya source")
			article.thumbnail_link = entry['source']['href']
			article.thumbnail_desc = entry['source']['title']
			
		elif 'media_content' in entry:
			print("arabiya media_content")
			article.thumbnail_link = entry['media_content'][0]['url']
			pub_date = dateutil.parser.parse(entry['published'])
			article.pub_date = pub_date
			article.thumbnail_desc = entry['title']

		elif 'summary_detail' in entry:
			print("arabiya thumbnail")
			# article.thumbnail_link = entry['thumbnail']
			article.thumbnail_desc = entry['summary_detail']['value']
			
		article.save()


def populate_articles_arabiya_sports():
	
	rss_link = rss_links[4]
	content_source = content_sources[4]
	feed = pull_xml(rss_link)
	print(feed.entries)
	for entry in feed.entries:
		
		article = Article.objects.get_or_create(title=entry['title'])[0]
		article.category = 'sports'
		# print(str(article.title))
		if entry['description']:
			article.description = entry['description']
		else:
			article.description = entry['title']

		article.article_link = entry['link']
		article.content_source = content_source

		if 'source' in entry:
			print("arabiya source")
			article.thumbnail_link = entry['source']['href']
			article.thumbnail_desc = entry['source']['title']
			
		elif 'media_content' in entry:
			print("arabiya media_content")
			article.thumbnail_link = entry['media_content'][0]['url']
			pub_date = dateutil.parser.parse(entry['published'])
			article.pub_date = pub_date
			article.thumbnail_desc = entry['title']

		elif 'summary_detail' in entry:
			print("arabiya thumbnail")
			# article.thumbnail_link = entry['thumbnail']
			article.thumbnail_desc = entry['summary_detail']['value']
			
		article.save()



def populate_articles_bbc_trending():
	
	rss_link = rss_links[5]
	content_source = content_sources[5]
	feed = pull_xml(rss_link)

	for entry in feed.entries:
		
		article = Article.objects.get_or_create(title=entry['title'])[0]
		article.category = 'trending'
		# print(str(article.title))
		if entry['description']:
			article.description = entry['description']
		else:
			article.description = entry['summary']['summary_detail']['value']

		article.article_link = entry['link']
		article.content_source = content_source

		if 'source' in entry:
			print("BBC source")
			article.thumbnail_link = entry['source']['href']
			article.thumbnail_desc = entry['source']['title']
			
		elif 'media_thumbnail' in entry:
			print("BBC media")
			article.thumbnail_link = entry['media_thumbnail'][0]['url']
			pub_date = dateutil.parser.parse(entry['published'])
			article.pub_date = pub_date

			if entry['summary_detail']['value']:
				article.thumbnail_desc = entry['summary_detail']['value']
			else:
				article.thumbnail_desc = ['media_thumbnail'][0]['title']

		elif 'summary_detail' in entry:
			print("BBC thumbnail")
			# article.thumbnail_link = entry['thumbnail']
			article.thumbnail_desc = entry['summary_detail']['value']
			
		article.save()


def populate_articles_arabiya_travel():
	
	rss_link = rss_links[6]
	content_source = content_sources[6]
	feed = pull_xml(rss_link)
	print(feed.entries)
	for entry in feed.entries:
		
		article = Article.objects.get_or_create(title=entry['title'])[0]
		article.category = 'travel'
		# print(str(article.title))
		if entry['description']:
			article.description = entry['description']
		else:
			article.description = entry['title']

		article.article_link = entry['link']
		article.content_source = content_source

		if 'source' in entry:
			print("arabiya travel source")
			article.thumbnail_link = entry['source']['href']
			article.thumbnail_desc = entry['source']['title']
			
		elif 'media_content' in entry:
			print("arabiya travel media_content")
			article.thumbnail_link = entry['media_content'][0]['url']
			pub_date = dateutil.parser.parse(entry['published'])
			article.pub_date = pub_date
			article.thumbnail_desc = entry['title']

		elif 'summary_detail' in entry:
			print("arabiya travel thumbnail")
			# article.thumbnail_link = entry['thumbnail']
			article.thumbnail_desc = entry['summary_detail']['value']
			
		article.save()

def populate_articles_arabiya_culture():
	
	rss_link = rss_links[7]
	content_source = content_sources[7]
	feed = pull_xml(rss_link)
	print(feed.entries)
	for entry in feed.entries:
		
		article = Article.objects.get_or_create(title=entry['title'])[0]
		article.category = 'culture'
		# print(str(article.title))
		if entry['description']:
			article.description = entry['description']
		else:
			article.description = entry['title']

		article.article_link = entry['link']
		article.content_source = content_source

		if 'source' in entry:
			print("arabiya culture source")
			article.thumbnail_link = entry['source']['href']
			article.thumbnail_desc = entry['source']['title']
			
		elif 'media_content' in entry:
			print("arabiya culture media_content")
			article.thumbnail_link = entry['media_content'][0]['url']
			pub_date = dateutil.parser.parse(entry['published'])
			article.pub_date = pub_date
			article.thumbnail_desc = entry['title']

		elif 'summary_detail' in entry:
			print("arabiya culture thumbnail")
			# article.thumbnail_link = entry['thumbnail']
			article.thumbnail_desc = entry['summary_detail']['value']
			
		article.save()

if __name__ == '__main__':
	print('starting population_script.py')
	# populate_articles_bbc_science_and_tech()
	# populate_articles_alhurra_tech()
	# populate_articles_bbc_world_news()
	# populate_articles_arabiya_health()
	# populate_articles_bbc_trending()
	# populate_articles_arabiya_travel()
	populate_articles_arabiya_culture()
	# populate_articles_arabiya_sports()
	
