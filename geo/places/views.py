from django.shortcuts import render
from serializers import CitySerializer
from rest_framework import viewsets
from .models import Place
from django.contrib.gis.geos import Point
from django.contrib.gis.measure import D

class PlacesViewset(viewsets.ModelViewSet):
    serializer_class = CitySerializer
    queryset = Place.objects.none()
    paginate_by = None

    def get_queryset(self):
        lat = self.request.GET.get('lat','')
        lng = self.request.GET.get('lng','')
        distance = self.request.GET.get('dist',10)
        pnt = Point(float(lng), float(lat))
        return Place.objects.filter(geom__distance_lte=(pnt, D(mi=distance)))