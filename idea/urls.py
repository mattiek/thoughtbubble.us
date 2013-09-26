from django.conf.urls import patterns, include, url
from views import IdeaList

urlpatterns = patterns('idea.views',
   url(r'^add/?$', 'addidea', name='addidea'),
   url(r'^add/(?P<id>\d+)/?$', 'addidea', name='addidea'),
   url(r'^$', IdeaList.as_view(), name='idea_list'),
)
