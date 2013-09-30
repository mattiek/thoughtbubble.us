from django.conf.urls import patterns, include, url
from views import CommunityList, CommunityDetail, CommunityCreate, CommunityUpdate

urlpatterns = patterns('community.views',
   url(r'^add/?$', CommunityCreate.as_view(), name='community_create'),
   url(r'^$', CommunityList.as_view(), name='community_list'),
   url(r'^(?P<state>\w+)/?$', CommunityList.as_view(), name='community_list'),
   url(r'^(?P<state>\w+)/(?P<city>\w+)/?$', CommunityList.as_view(), name='community_list'),
   url(r'^(?P<state>\w+)/(?P<city>\w+)/(?P<pk>\d+)/?$', CommunityDetail.as_view(), name='community_detail'),
   url(r'^(?P<state>\w+)/(?P<city>\w+)/(?P<pk>\d+)/join/?$', 'join_from_community', name='community_join'),
   url(r'^(?P<state>\w+)/(?P<city>\w+)/(?P<pk>\d+)/edit/?$', CommunityUpdate.as_view(), name='community_update'),

   )
