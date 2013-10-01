from django.conf.urls import patterns, include, url
from views import IdeaList, IdeaDetail, IdeaCreate

urlpatterns = patterns('idea.views',
   url(r'^add/?$', 'addidea', name='addidea'),
   url(r'^adds/?$', IdeaCreate.as_view(), name='addideas'),
   url(r'^add/(?P<id>\d+)/?$', 'addidea', name='addidea'),
   url(r'^support/(?P<id>\d+)/?$', 'support_idea', name='support_idea'),
   url(r'^$', IdeaList.as_view(), name='idea_list'),
   url(r'^(?P<state>\w+)/?$', IdeaList.as_view(), name='idea_list'),
   url(r'^(?P<state>\w+)/(?P<city>\w+)/?$', IdeaList.as_view(), name='idea_list'),
   url(r'^(?P<state>\w+)/(?P<city>\w+)/(?P<community>[-\w]+)/?$', IdeaList.as_view(), name='idea_list'),
   url(r'^(?P<state>\w+)/(?P<city>\w+)/(?P<community>[-\w]+)/(?P<pk>\d+)/?$', IdeaDetail.as_view(), name='idea_detail'),
)
