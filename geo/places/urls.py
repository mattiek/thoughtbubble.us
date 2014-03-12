from django.conf.urls import patterns, include, url
from views import PlacesList, PlacesDetail, PlacesCreate, PlacesUpdate

urlpatterns = patterns('geo.places.views',
   url(r'^add/?$', PlacesCreate.as_view(), name='places_create'),
   # url(r'^$', OrganizationList.as_view(), name='organization_list'),
   # url(r'^(?P<state>\w+)/?$', OrganizationList.as_view(), name='organization_list'),
   url(r'^list/?$', PlacesList.as_view(), name='places_list'),
   url(r'^detail/(?P<place>[\w-]+)/?$', PlacesDetail.as_view(), name='places_detail'),
   )
