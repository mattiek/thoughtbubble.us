from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from models import City
from serializers import CitySerializer
from rest_framework import viewsets
from django.shortcuts import render

from rest_framework import generics


class CityViewset(viewsets.ModelViewSet):
    serializer_class = CitySerializer
    queryset = City.objects.none()

    def get_queryset(self):
        name = self.request.GET.get('city','')
        state = self.request.GET.get('state','')
        return City.objects.filter(name__icontains=name, state_code__icontains=state)

