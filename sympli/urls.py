from django.conf.urls import url, include
from sympli import views
from django.conf import settings
from django.conf.urls.static import static

app_name='sympli'

urlpatterns=[
	url(r'^$', views.index, name='index'),
	url(r'^world/$', views.world, name='world'),
	url(r'^us/$', views.us, name='us'),
	url(r'^tech/$', views.tech, name='tech'),
	url(r'^health/$', views.health, name='health'),
	url(r'^trending/$', views.trending, name='trending'),
	url(r'^travel/$', views.travel, name='travel'),
	url(r'^culture/$', views.culture, name='culture'),
	url(r'^sport/$', views.sport, name='sport'),
	url(r'^variety/$', views.variety, name='variety'),
	url(r'^(?P<category>world|^$|tech|us|health|trending|travel|culture|sport|variety)/(?P<article_id>[\w\-]+)/', views.show_article, name="show_article"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)