from django.conf.urls import url, include
from sympli import views
from django.conf import settings
from django.conf.urls.static import static

app_name='sympli'

urlpatterns=[
	url(r'^$', views.index, name='index'),
	url(r'^worldnews/$', views.worldnews, name='worldnews'),
	url(r'^science_and_tech/$', views.science_and_tech, name='science_and_tech'),
	url(r'^health/$', views.health, name='health'),
	url(r'^trending/$', views.trending, name='trending'),
	url(r'^travel/$', views.travel, name='travel'),
	url(r'^culture/$', views.culture, name='culture'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)