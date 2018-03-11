#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sympli_proj.settings')
import django
django.setup()
from django.utils import timezone
import feedparser
from sympli.models import ContentSource, Article
import dateutil.parser
from datetime import date, datetime, timedelta
import pytz

def pull_xml(rss_link):
	news_feed = feedparser.parse(rss_link)
	return news_feed

def content_sources():
	rss_links = ['http://feeds.bbci.co.uk/news/world/rss.xml?edition=uk',
	'http://feeds.bbci.co.uk/news/technology/rss.xml?edition=uk',
	'http://feeds.bbci.co.uk/news/health/rss.xml?edition=uk',
	'http://abcnews.go.com/abcnews/usheadlines',
	'http://abcnews.go.com/abcnews/healthheadlines',
	'http://abcnews.go.com/abcnews/travelheadlines',
	'http://abcnews.go.com/abcnews/sportsheadlines'
	,'http://abcnews.go.com/abcnews/technologyheadlines',
	'http://abcnews.go.com/abcnews/politicsheadlines',
	'http://abcnews.go.com/abcnews/gmaheadlines',
	'http://abcnews.go.com/abcnews/nightlineheadlines',
	'http://abcnews.go.com/abcnews/2020headlines',
	'http://abcnews.go.com/abcnews/thisweekheadlines',
	'http://abcnews.go.com/abcnews/primetimeheadlines',
	'https://www.newyorker.com/feed/culture',
	'https://www.newyorker.com/feed/tech',
	'https://www.newyorker.com/feed/news/sporting-scene',
	'https://www.newyorker.com/feed/news']
	return rss_links

#GLOBAL VARIABLE

rss_links = content_sources()

def populate_content_sources():

	content_sources = []

	for rss_link in rss_links:
		feed = pull_xml(rss_link)
		print(feed)
		content_source = ContentSource.objects.get_or_create(link = rss_link)[0]
		
		content_source.title = feed['channel']['title']
		content_source.description = feed['channel']['description']
		

		
		
		if 'SWI' in content_source.description:
			content_source.logo_title = feed['channel']['description']
			content_source.logo_image = 'logo_images/-swi-swissinfoch.jpg'
			# elif "Alhurra" in content_source.description:
			# 	content_source.logo_title = feed['channel']['description']
			# 	content_source.logo_link = 'https://thesinosaudiblog.files.wordpress.com/2009/12/al-hurra.jpg'
		elif "CNN.com" in content_source.title:
			content_source.logo_title = feed['channel']['description']
			content_source.logo_link = "https://vignette.wikia.nocookie.net/future/images/a/ad/CNN_Logo.jpg/revision/latest?cb=20120208025030"
		elif 'The New Yorker' in content_source.description:
			content_source.logo_title = feed['channel']['description']
			content_source.logo_link = 'http://16896-presscdn-0-13.pagely.netdna-cdn.com/wp-content/uploads/tny.jpg'
			
		else:
			content_source.logo_title = feed['feed']['title']
			try:
				content_source.logo_link = feed['feed']['image']['href']
			except Exception as e:
				print("HREFF: "+ str(e))
				content_source.logo_link = feed['feed']['image']['url']
			else:
				pass
			finally:
				pass
			
			


		content_source.save()

		content_sources.append(content_source)

	return content_sources

# GLOBAL VARIABLE
content_sources = populate_content_sources()

def populate_articles():
	categories = ['world','tech', 'health', 'us', 'health', 'travel','sport','tech','us','us',
	'us','us','us','us','travel','culture','tech',
	'sport','us']

	for i in range(len(rss_links)):
		rss_link = rss_links[i]
		content_source = content_sources[i]
		feed = pull_xml(rss_link)
		

		for entry in feed.entries:
			# print(str(entry['published']))
			article = Article.objects.get_or_create(title=entry['title'])[0]

			article.category = categories[i]
			article.description = entry['title']
			article.article_link = entry['link']
			article.content_source = content_source
			try:
				pub_date = str(dateutil.parser.parse(entry['published'], fuzzy = True))
				print('This is what they want! ' + str(article.article_link))
			except Exception as e:
				print("This is DATE " + str(pub_date))
				pub_date = str(pub_date)
				print("This is new DATE " + pub_date)
				print("DATE ERROR" + str(e))
			
			article.pub_date = pub_date
			article.thumbnail_desc = entry['title']

			if 'media_content' in entry:#for arabiya articles
				try:
					article.thumbnail_link = entry['media_content'][0]['url']
				except Exception as e:
					try:
						article.thumbnail_link = entry["media_thumbnail"][0]["url"]#this is for new yorker
					except Exception as e:
						continue
				
				
			elif 'media_thumbnail' in entry:#for bbc articles
				article.thumbnail_link = entry['media_thumbnail'][0]['url']

			elif "links" in entry:#for hurra articles
				try:
					article.thumbnail_link = entry['links'][1]['href']
				except IndexError:
					continue
				
			else:
				print("XXXXXXXXXXXXXXXXXXXXXXXXXXXX" + str(entry))
				continue

			if article.pub_date is not None:
				article.save()
			

def delete_old_articles():
	time_benchmark = timezone.now()-timedelta(days=6)
	old_articles = Article.objects.all()
	for art in old_articles:
		if art.pub_date <= time_benchmark:
			art.delete()

def delete_bad_articles():# articles that don't have links and other important details
	bad_articles = Article.objects.filter(article_link='')
	for bad_article in bad_articles:
		bad_article.delete()
		print("deleted a baddie")


if __name__ == '__main__':
	print('starting population_script.py')
	populate_articles()
	# delete_bad_articles()
	delete_old_articles()
