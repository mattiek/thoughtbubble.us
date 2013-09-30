from django.conf.urls import patterns, include, url
from views import LocationList, LocationCreate, LocationDetail

urlpatterns = patterns('location.views',
   # url(r'^add/?$', 'addlocation', name='addlocation'),
   url(r'^add/?$', LocationCreate.as_view(), name='addlocation'),
   url(r'^$', LocationList.as_view(), name='location_list'),
   url(r'^view/(?P<pk>\d+)$', LocationDetail.as_view(), name='location_detail'),
)
