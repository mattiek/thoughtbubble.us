from django.conf.urls import patterns, include, url
from rest_framework import routers
from cities.views import CityViewset
from location.views import LocationViewset
import location

router = routers.DefaultRouter()
router.register(r'locations', location.views.LocationViewset)
router.register(r'cities', CityViewset)

urlpatterns = patterns('',
                       # Examples:
                       url(r'^v1/', include(router.urls)),
                       url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework'))
)


