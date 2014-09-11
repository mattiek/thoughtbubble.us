from django.contrib.gis.geoip import GeoIP
from geo.places.utils import get_region_from_geoip
from geo.places.models import Region

class GeoIPMiddleware(object):

    def __init__(self):
        pass

    def get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip

    def process_request(self, request):
        request.session['ip'] = self.get_client_ip(request)
        if not request.session.get('region', None):
            g = GeoIP()
            city = g.city(self.get_client_ip(request))
            request.geoip = city
            p = get_region_from_geoip(request.geoip)
            if not p:
                p = Region.objects.get(name__iexact='central')
            request.session['region'] = p






