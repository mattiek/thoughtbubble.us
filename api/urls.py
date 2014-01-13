from django.conf.urls import patterns, include, url
from rest_framework import routers
from cities.views import CityViewset,CityTypeaheadViewset
from location.views import LocationViewset
from organization.views import OrganizationViewset
import location

router = routers.DefaultRouter()
# api = router.SimpleRouter()

router.register(r'locations', location.views.LocationViewset, base_name="locations")
router.register(r'cities', CityViewset)
router.register(r'cities-typeahead', CityTypeaheadViewset)
router.register(r'organizations', OrganizationViewset)

urlpatterns = patterns('',
                       # Examples:
                       url(r'^v1/', include(router.urls)),
                       url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework'))
)


