from django.conf.urls import url, include
from sympli import views
from django.conf import settings
from django.conf.urls.static import static

app_name='sympli'

urlpatterns=[
	url(r'^$', views.index, name='index'),
	url(r'^أخبار_العالم/$', views.worldnews, name='world_news'),
	url(r'^علوم_و_تكنولوجيا/$', views.science_and_tech, name='science_and_tech'),
	url(r'^صحه/$', views.health, name='health'),
	url(r'^ترند/$', views.trending, name='trending'),
	url(r'^سياحه_و_سفر/$', views.travel, name='travel'),
	url(r'^ثقافه/$', views.culture, name='culture'),
	url(r'^رياضه/$', views.sport, name='sport'),
	url(r'^منوعات/$', views.variety, name='variety'),
	url(r'^(?P<category>أخبار_العالم|^$|علوم_و_تكنولوجيا|صحه|ترند|سياحه_و_سفر|ثقافه|رياضه|منوعات)/(?P<article_id>[\w\-]+)/', views.show_article, name="show_article"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)