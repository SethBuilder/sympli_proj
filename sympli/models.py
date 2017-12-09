# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.core.files import File
import os
import urllib
from django.template.defaultfilters import slugify
import requests
from time import sleep
from langdetect import detect
from urllib.parse import urlsplit, urlunsplit

def slugify_arabic(str):
		str = str.replace(" ", "-")
		str = str.replace(",", "-")
		str = str.replace("(", "-")
		str = str.replace(")", "")
		str = str.replace("؟", "")
		str = str.replace("\"", "-")
		str = str.replace("\'", "-")
		str = str.replace("|", "-")
		str = str.replace("/", "-")
		str = str.replace("\\", "-")
		return str


def pull_logo_image(logo_link, file_name):					
	#retrieve the profile pic
	try:
		retrieved_image = requests.get(logo_link)
		# sleep(3)#To avoid jamming the requests library
		image = retrieved_image.content
		
	except requests.exceptions.ConnectionError as e:
		e.status_code = 'Connection refused'
		print(e.status_code)
		
		#If requests throws exception use this alternative city image
		# retrieved_image = open('/home/excurj/excurj_proj/static/images/one.jpg', 'rb').read()
		# image = retrieved_image
	try:
		#create local file to save remote image
		with open(file_name, 'wb') as f:
			#write the remote image to the local file we just created
			f.write(image)


		reopen = open(file_name, 'rb')
		django_file = File(reopen)
	except FileNotFoundError as e: 
		print("ERRROR AT 49 is: " + str(e))
		file_name = 'notfound.jpg'
		reopen = open(file_name, 'rb')
		django_file = File(reopen)

	return django_file

class ContentSource(models.Model):
	title = models.CharField(max_length=1000, blank=True)
	description = models.CharField(max_length=10000, blank=True)
	logo_image = models.ImageField(blank=True, upload_to='logo_images')
	logo_link =models.URLField(blank=True)
	logo_title = models.CharField(max_length=1000, blank=True)
	logo_title_slug = models.SlugField()
	link = models.URLField(blank=True)
	last_updated = models.DateField(blank=True, default=timezone.now)

	#Override save to save logo image

	def save(self, *args, **kwargs):
		if not self.logo_image and self.logo_link:
			# pdb.set_trace()
			self.logo_title_slug = slugify(self.logo_title)
			print(self.logo_title_slug)
			file_name = self.logo_title_slug +'.jpg'
			print(file_name)
			django_file = pull_logo_image(self.logo_link, file_name)
			self.logo_image.save(file_name, django_file, save=True)
			django_file.close()
			try:
				#delete local files as they're already uploaded to media root
				if os.path.isfile(self.logo_title_slug+'.jpg'):
					os.remove(self.logo_title_slug+'.jpg')
					print("removed: " + self.logo_title_slug+'.jpg')
			except FileNotFoundError:
				pass

		super(ContentSource, self).save(*args, **kwargs)

class Article(models.Model):
	title = models.CharField(max_length=10000, blank=True)
	description = models.CharField(max_length=50000, blank=True)
	article_link = models.URLField()
	thumbnail_link = models.URLField(blank=True, max_length=5000)
	thumbnail_desc = models.CharField(blank=True, max_length=15000)
	thumbnail_image = models.ImageField(blank=True, upload_to='article_thumbnails', max_length=5000)
	thumbnail_desc_slug = models.SlugField(default='test-slug-ar', allow_unicode=True, max_length=600)
	content_source = models.ForeignKey(ContentSource, default=1)
	pub_date = models.DateTimeField(blank=True, null=True)
	category = models.CharField(blank=True, max_length=100)
	# likes = models.ManyToManyField(Like, default=0)

	#Override save to save logo image and convert http to https
	def save(self, *args, **kwargs):
		self.article_link = urlsplit(self.article_link)
		self.article_link = self.article_link._replace(scheme='https')
		self.article_link = urlunsplit(self.article_link)
		
		if not self.thumbnail_image and self.thumbnail_link:
			# pdb.set_trace()
			if str(detect(self.thumbnail_desc)) == 'ar':
				desc_for_slug = self.thumbnail_desc.split()[:5]
				desc_for_slug = ('-').join(desc_for_slug)

				self.thumbnail_desc_slug = slugify_arabic(desc_for_slug)

			else:
				desc_for_slug = self.thumbnail_desc.split()[:5]
				desc_for_slug = (' ').join(desc_for_slug)
				self.thumbnail_desc_slug = slugify(desc_for_slug)

			file_name = self.thumbnail_desc_slug +'.jpg'

			try:
				django_file = pull_logo_image(self.thumbnail_link, file_name)
				self.thumbnail_image.save(file_name, django_file, save=True)
				
			except FileNotFoundError as e:
				print("ERROR AT 113" + str(e))
				file_name = 'notfound.jpg'
				django_file = pull_logo_image(self.thumbnail_link, file_name)
				self.thumbnail_image.save(file_name, django_file, save=True)

			finally:
				django_file.close()

			#delete local files as they're already uploaded to media root
			if os.path.isfile(self.thumbnail_desc_slug+'.jpg'):
				os.remove(self.thumbnail_desc_slug+'.jpg')
				print("removed: " + self.thumbnail_desc_slug+'.jpg')

		super(Article, self).save(*args, **kwargs)

class Like(models.Model):
	author = models.ForeignKey(User)
	liked_article = models.ForeignKey(Article)

class Interest(models.Model):
	name = models.CharField(max_length=100, blank=True)
	frequency = models.FloatField(blank=True)

class ArticleKeyword(models.Model):
	name = models.CharField(max_length=100, blank=True)
	frequency = models.FloatField(blank=True)

class Magazine(models.Model):
	author = models.ForeignKey(User)
	content = models.ManyToManyField(Article, blank=True)

class UserProfile(models.Model):
	"""Each User instance is associated with a profile instance - One to One"""
	user = models.OneToOneField(User, related_name='profile', primary_key=True)
	prof_pic = models.ImageField(blank=True, upload_to='prof_pictures')
	interests = models.ManyToManyField(Interest, blank=True)
	magazines = models.ManyToManyField(Magazine, blank=True)
	liked_articles = models.ManyToManyField(Like, default=0)
	def __str__(self):
		return self.user.first_name



