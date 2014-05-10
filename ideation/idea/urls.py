from django.conf.urls import patterns, include, url
from views import IdeaList, IdeaDetail, IdeaCreate

urlpatterns = patterns('ideation.idea.views',

   url(r'^flag/(?P<idea>[\w-]+)/?$', 'flag_idea', name='flag_idea'),
   url(r'^support/(?P<idea>[\w-]+)/?$', 'support_idea', name='support_idea'),
   url(r'^supporting/(?P<idea>[\w-]+)/?$', 'support_idea_from_detail', name='support_idea_from_detail'),

   url(r'^add/?$', 'addidea', name='addidea'),
   url(r'^add/(?P<place>[\w-]+)$', 'addidea', name='addidea'),
   url(r'^add/(?P<place>[\w-]+)/(?P<organization>[\w-]+)$', 'addidea', name='addidea'),
   url(r'^add/(?P<place>[\w-]+)/(?P<organization>[\w-]+)/(?P<location>[\w-]+)$', 'addidea', name='addidea'),

   url(r'^list/?$', IdeaList.as_view(), name='idea_list'),
   url(r'^list/(?P<place>[\w-]+)/(?P<organization>[\w-]+)/?$', IdeaList.as_view(), name='idea_list'),
   url(r'^list/(?P<place>[\w-]+)/(?P<organization>[\w-]+)/(?P<location>[\w-]+)/?$', IdeaList.as_view(), name='idea_list'),

   url(r'^detail/(?P<place>[\w-]+)/(?P<idea>[\w-]+)/?$', IdeaDetail.as_view(), name='place_idea_detail'),
   url(r'^detail/(?P<place>[\w-]+)/(?P<organization>[\w-]+)/(?P<location>[\w-]+)/(?P<idea>[\w-]+)/?$', IdeaDetail.as_view(), name='idea_detail'),

   # url(r'^$', IdeaList.as_view(), name='idea_list'),
   # url(r'^(?P<state>\w+)/?$', IdeaList.as_view(), name='idea_list'),
   # url(r'^$', IdeaList.as_view(), name='idea_list'),
  )
