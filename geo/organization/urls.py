from django.conf.urls import patterns, include, url
from views import OrganizationList, OrganizationDetail, OrganizationCreate, OrganizationUpdate

urlpatterns = patterns('geo.organization.views',
   url(r'^add/?$', OrganizationCreate.as_view(), name='organization_create'),
   # url(r'^$', OrganizationList.as_view(), name='organization_list'),
   # url(r'^(?P<state>\w+)/?$', OrganizationList.as_view(), name='organization_list'),
   url(r'^list/?$', OrganizationList.as_view(), name='organization_list'),
   url(r'^detail/(?P<place>[\w-]+)/(?P<organization>[\w-]+)/?$', OrganizationDetail.as_view(), name='organization_detail'),
   url(r'^join/(?P<place>[\w-]+)/(?P<organization>[\w-]+)/?$', 'join_from_organization', name='organization_join'),
   url(r'^edit/(?P<place>[\w-]+)/(?P<organization>[\w-]+)/?$', OrganizationUpdate.as_view(), name='organization_update'),

   )
