from django.conf.urls import patterns, include, url
from views import NeighborhoodDetail

urlpatterns = patterns('neighborhood.views',
   # url(r'^add/?$', OrganizationCreate.as_view(), name='organization_create'),
   # url(r'^$', OrganizationList.as_view(), name='organization_list'),
   # url(r'^(?P<state>\w+)/?$', OrganizationList.as_view(), name='organization_list'),
   # url(r'^$', OrganizationList.as_view(), name='organization_list'),
   url(r'^(?P<pk>\d+)/?$', NeighborhoodDetail.as_view(), name='neighborhood_detail'),
   # url(r'^(?P<pk>\d+)/join/?$', 'join_from_organization', name='organization_join'),
   # url(r'^(?P<pk>\d+)/edit/?$', OrganizationUpdate.as_view(), name='organization_update'),

   )
