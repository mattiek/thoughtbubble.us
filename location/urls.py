from django.conf.urls import patterns, include, url
from views import LocationList

urlpatterns = patterns('location.views',
   url(r'^add/?$', 'addlocation', name='addlocation'),
   url(r'^$', LocationList.as_view(), name='location_list'),
)
