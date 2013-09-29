from django.conf.urls import patterns, include, url
from views import LocationList, LocationCreate

urlpatterns = patterns('location.views',
   # url(r'^add/?$', 'addlocation', name='addlocation'),
   url(r'^add/?$', LocationCreate.as_view(), name='addlocation'),
   url(r'^$', LocationList.as_view(), name='location_list'),
)
