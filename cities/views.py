from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from models import City
from serializers import CitySerializer
from rest_framework import viewsets
from django.shortcuts import render

from rest_framework import generics
from django.contrib.gis.geos import Point
from django.contrib.gis.measure import D



class CityViewset(viewsets.ModelViewSet):
    serializer_class = CitySerializer
    queryset = City.objects.none()
    paginate_by = None

    def get_queryset(self):
        lat = self.request.GET.get('lat','')
        lng = self.request.GET.get('lng','')
        distance = self.request.GET.get('dist',10)
        pnt = Point(float(lng), float(lat))
        return City.objects.filter(geom__distance_lte=(pnt, D(mi=distance)))


class CityTypeaheadViewset(viewsets.ModelViewSet):
    serializer_class = CitySerializer
    queryset = City.objects.none()
    paginate_by = None

    def get_queryset(self):
        name = self.request.GET.get('city','')
        state = self.request.GET.get('state','')
        max_results = self.request.GET.get('max','10')
        offset = self.request.GET.get('offset','0')
        return City.objects.filter(name__icontains=name, state_code__icontains=state)[offset:max_results]

