from django.shortcuts import render
from serializers import CitySerializer
from rest_framework import viewsets
from .models import Place
from django.contrib.gis.geos import Point
from django.contrib.gis.measure import D
from django.contrib.gis.geos import fromstr
from django.contrib.gis.geos import Polygon

class PlacesViewset(viewsets.ModelViewSet):
    serializer_class = CitySerializer
    queryset = Place.objects.none()
    paginate_by = None

    def get_queryset(self):
        lat = self.request.GET.get('lat','')
        lng = self.request.GET.get('lng','')
        distance = self.request.GET.get('dist',10)
        pnt = Point(float(lng), float(lat))

        bb = self.request.GET.get('bb','')
        if bb:
            bounds = bb.split(',')

            bounds = map(lambda i: float(i),bounds)

            poly = Polygon( (
                                (bounds[0], bounds[1]),
                                (bounds[2], bounds[1]),
                                (bounds[2], bounds[3]),
                                (bounds[0], bounds[3]),
                                (bounds[0], bounds[1]),
                             ) )

            # poly_str = "POLYGON ( %s %s %s %s %s %s %s %s)" % ( str(bounds[0]), str(bounds[1]),
            #                                                     str(bounds[2]), str(bounds[1]),
            #                                                     str(bounds[2]), str(bounds[3]),
            #                                                     str(bounds[0]),str( bounds[3]),
            # )
            #
            # print poly_str
            #
            # bounding_box = fromstr(poly_str)


        return Place.objects.distance(pnt).order_by('distance').filter(geom__within=poly)[:50]