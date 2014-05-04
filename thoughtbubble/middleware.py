from django.contrib.gis.geoip import GeoIP

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
        g = GeoIP()
        city = g.city(self.get_client_ip(request))
        request.geoip = city