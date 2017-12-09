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
	rss_links = ['https://arabic.cnn.com/rss','http://feeds.bbci.co.uk/arabic/scienceandtech/rss.xml','http://feeds.bbci.co.uk/arabic/world/rss.xml', 
	'https://www.alhurra.com/api/z-gvev_qt','https://www.alarabiya.net/.mrss/ar/medicine-and-health.xml', 'http://feeds.bbci.co.uk/arabic/trending/rss.xml', 
	'https://www.alarabiya.net/.mrss/ar/aswaq/travel-and-tourism.xml', 'https://www.alarabiya.net/.mrss/ar/culture-and-art.xml', 
	'http://www.aljazeera.net/aljazeerarss/9ff80bf7-97cf-47f2-8578-5a9df7842311/497f8f74-88e0-480d-b5d9-5bfae29c9a63',]
	return rss_links

#GLOBAL VARIABLE
rss_links = content_sources()

def populate_content_sources():

	content_sources = []

	for rss_link in rss_links:
		feed = pull_xml(rss_link)
		if rss_link == 'http://www.aljazeera.net/aljazeerarss/9ff80bf7-97cf-47f2-8578-5a9df7842311/497f8f74-88e0-480d-b5d9-5bfae29c9a63':
			print(feed)
		content_source = ContentSource.objects.get_or_create(link = rss_link)[0]
		
		content_source.title = feed['channel']['title']
		content_source.description = feed['channel']['description']
		

		if 'AlArabiya' in content_source.description:
			content_source.logo_title = feed['channel']['description']
			content_source.logo_link = 'http://www.mbc.net/en/corporate/about-us/main/014/imageBinary/078d3a4e68b13c2ea0977a8547541de6b6d941ba/Alarabeya.net.jpg' 
		elif 'CNN' in content_source.description:
			content_source.logo_title = feed['channel']['description']
			content_source.logo_link = 'https://i.cdn.turner.com/dr/cnnarabic/cnnarabic/release/sites/all/themes/cnnarabic/zurb-foundation/images/navbar/logo.png'
		elif "BBC" in content_source.description:
			content_source.logo_title = feed['channel']['description']
			content_source.logo_link = 'https://www.broadbandtvnews.com/wp-content/uploads/2017/10/BBC-arabic.png'
		elif "Alhurra" in content_source.description:
			content_source.logo_title = feed['channel']['description']
			content_source.logo_link = 'https://www.alhurra.com/Content/responsive/MBN/ar-ALH/img/logo-print.gif'
			
		else:
			content_source.logo_title = feed['feed']['title']
			content_source.logo_link = feed['feed']['image']['href']
			


		content_source.save()

		content_sources.append(content_source)

	return content_sources

#GLOBAL VARIABLE
content_sources = populate_content_sources()

def populate_articles():
	categories = ['world_news','science_and_tech', 'world_news', 'science_and_tech', 'health', 'trending', 'travel', 'culture', 'world_news',]
	for i in range(len(rss_links)):
		rss_link = rss_links[i]
		content_source = content_sources[i]
		feed = pull_xml(rss_link)
		

		for entry in feed.entries:
			article = Article.objects.get_or_create(title=entry['title'])[0]

			article.category = categories[i]
			article.description = entry['title']
			article.article_link = entry['link']
			article.content_source = content_source
			pub_date = dateutil.parser.parse(entry['published'])
			article.pub_date = pub_date
			article.thumbnail_desc = entry['title']

			if 'media_content' in entry:#for arabiya articles
				article.thumbnail_link = entry['media_content'][0]['url']
				
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

			article.save()
			

def delete_bad_articles():# articles that don't have links and other important details
	bad_articles = Article.objects.filter(article_link='')
	for bad_article in bad_articles:
		bad_article.delete()
		print("deleted a baddie")


if __name__ == '__main__':
	print('starting population_script.py')
	populate_articles()
	delete_bad_articles()
	
