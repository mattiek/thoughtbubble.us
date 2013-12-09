from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from models import City
from serializers import CitySerializer
from rest_framework import viewsets
from django.shortcuts import render

from rest_framework import generics
from django.contrib.gis.geos import Point
from django.contrib.gis.measure import D
from vanilla import DetailView, CreateView, UpdateView, ListView
from idea.models import Idea


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
        typeahead = self.request.GET.get('typeahead','')

        if typeahead:
            d = typeahead.split(',')
            city = d[0]
            try:
                state = d[1]
            except:
                pass
            return City.objects.filter(name__icontains=city, state_code__icontains=state)[offset:max_results]
        return City.objects.filter(name__icontains=name, state_code__icontains=state)[offset:max_results]

class CityDetailView(DetailView):
    model = City

    def get_context_data(self, **kwargs):
        context = super(CityDetailView, self).get_context_data(**kwargs)

        context['ideas'] = Idea.objects.filter(content_type__name='cities', object_id=self.object.id)
        return context