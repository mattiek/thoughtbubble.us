from django.conf.urls import patterns, include, url
from views import LocationList, LocationCreate, LocationDetail, LocationUpdate

urlpatterns = patterns('location.views',
   # url(r'^add/?$', 'addlocation', name='addlocation'),
   # url(r'^add/?$', LocationCreate.as_view(), name='addlocation'),
   url(r'^(?P<community>\d+)/add/?$', LocationCreate.as_view(), name='addlocation'),
   url(r'^$', LocationList.as_view(), name='location_list'),
   url(r'^(?P<pk>\d+)/?$', LocationDetail.as_view(), name='location_detail'),
   url(r'^(?P<pk>\d+)/edit/?$', LocationUpdate.as_view(), name='location_update'),
)
