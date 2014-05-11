from django.contrib.gis.geoip import GeoIP
from django.contrib.gis.geos import Point
from django.contrib.gis.measure import D
from geo.places.models import Place, Region

def get_region_from_geoip(geoip=None):
    if not geoip:
        g = GeoIP()
        ip='71.74.93.236'
        geoip = g.city(ip)

    lat = geoip['latitude']
    lng = geoip['longitude']
    pnt = Point(lng,lat)
    places = Place.objects.filter(geom__distance_lt=(pnt, D(mi=50)))

    if places:
        place = places.distance(pnt).order_by('distance')[0]
        region = Region.objects.filter(counties=place.county_fk)
        return region

    return None