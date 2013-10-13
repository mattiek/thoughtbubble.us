from django.conf.urls import patterns, include, url
from views import IdeaList, IdeaDetail, IdeaCreate

urlpatterns = patterns('idea.views',
   url(r'^add/?$', 'addidea', name='addidea'),
   url(r'^adds/?$', IdeaCreate.as_view(), name='addideas'),
   url(r'^add/(?P<id>\d+)/?$', 'addidea', name='addidea'),
   url(r'^support/(?P<id>\d+)/?$', 'support_idea', name='support_idea'),
   url(r'^supporting/(?P<id>\d+)/?$', 'support_idea_from_detail', name='support_idea_from_detail'),
   url(r'^$', IdeaList.as_view(), name='idea_list'),
   # url(r'^(?P<state>\w+)/?$', IdeaList.as_view(), name='idea_list'),
   # url(r'^$', IdeaList.as_view(), name='idea_list'),
   url(r'^(?P<community>[-%\w ]+)/?$', IdeaList.as_view(), name='idea_list'),
   url(r'^(?P<community>[-%\w ]+)/(?P<pk>\d+)/?$', IdeaDetail.as_view(), name='idea_detail'),
)
