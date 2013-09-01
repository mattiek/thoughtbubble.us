from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from models import Location
from serializers import LocationSerializer
from rest_framework import viewsets
from django.shortcuts import render
from forms import AddLocationForm

from rest_framework import generics


class LocationViewset(viewsets.ModelViewSet):
    serializer_class = LocationSerializer
    queryset = Location.objects.none()

    def get_queryset(self):
        name = self.request.GET.get('city','')
        return Location.objects.filter(name__icontains=name)


def addlocation(request):
    form = AddLocationForm()
    return render(request, 'add.html', {'form': form})