from django.conf.urls import patterns, include, url
from views import CommunityList, CommunityDetail, CommunityCreate

urlpatterns = patterns('community.views',
   url(r'^add/?$', CommunityCreate.as_view(), name='community_create'),
   # url(r'^add/(?P<id>\d+)/?$', 'addidea', name='addidea'),
   # url(r'^support/(?P<id>\d+)/?$', 'support_idea', name='support_idea'),
   url(r'^$', CommunityList.as_view(), name='community_list'),
   url(r'^(?P<state>\w+)/?$', CommunityList.as_view(), name='community_list'),
   url(r'^(?P<state>\w+)/(?P<city>\w+)/?$', CommunityList.as_view(), name='community_list'),
   url(r'^(?P<state>\w+)/(?P<city>\w+)/(?P<pk>\d+)/?$', CommunityDetail.as_view(), name='community_detail'),
   url(r'^(?P<state>\w+)/(?P<city>\w+)/(?P<pk>\d+)/join/?$', 'join_from_community', name='community_join'),
   )
