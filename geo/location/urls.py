from django.conf.urls import patterns, include, url
from views import LocationList, LocationCreate, LocationDetail, LocationUpdate

urlpatterns = patterns('geo.location.views',
   # url(r'^add/?$', 'addlocation', name='addlocation'),
   # url(r'^add/?$', LocationCreate.as_view(), name='addlocation'),
   url(r'^(?P<organization>[\w-]+)/add/?$', LocationCreate.as_view(), name='addlocation'),
   url(r'^$', LocationList.as_view(), name='location_list'),
   url(r'^(?P<location>[\w-]+)/?$', LocationDetail.as_view(), name='location_detail'),
   url(r'^(?P<location>[\w-]+)/edit/?$', LocationUpdate.as_view(), name='location_update'),
)
