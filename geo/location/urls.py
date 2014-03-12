from django.conf.urls import patterns, include, url
from views import LocationList, LocationCreate, LocationDetail, LocationUpdate

urlpatterns = patterns('geo.location.views',
   # url(r'^add/?$', 'addlocation', name='addlocation'),
   # url(r'^add/?$', LocationCreate.as_view(), name='addlocation'),
   url(r'^add/(?P<organization>[\w-]+)/?$', LocationCreate.as_view(), name='addlocation'),
   url(r'^list/?$', LocationList.as_view(), name='location_list'),
   url(r'^detail/(?P<place>[\w-]+)/(?P<organization>[\w-]+)/(?P<location>[\w-]+)/?$', LocationDetail.as_view(), name='location_detail'),
   url(r'^edit/(?P<place>[\w-]+)/(?P<organization>[\w-]+)/(?P<location>[\w-]+)/?$', LocationUpdate.as_view(), name='location_update'),
)
