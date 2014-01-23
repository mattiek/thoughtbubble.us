from django.conf.urls import patterns, include, url
from rest_framework import routers
# from geo.cities.views import CityViewset,CityTypeaheadViewset
from geo.places.views import PlacesViewset
from geo.location.views import LocationViewset
from geo.organization.views import OrganizationViewset
import geo.location

router = routers.DefaultRouter()
# api = router.SimpleRouter()

router.register(r'locations', geo.location.views.LocationViewset, base_name="locations")
# router.register(r'cities', CityViewset)
router.register(r'places', PlacesViewset)
# router.register(r'cities-typeahead', CityTypeaheadViewset)
router.register(r'organizations', OrganizationViewset)

urlpatterns = patterns('',
                       # Examples:
                       url(r'^v1/', include(router.urls)),
                       url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework'))
)


