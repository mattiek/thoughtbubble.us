from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from models import Location, LocationType
from serializers import LocationSerializer
from rest_framework import viewsets
from django.shortcuts import render, redirect
from forms import AddLocationForm
from django.contrib.gis.geos import GEOSGeometry
from django.contrib import messages

from rest_framework import generics

from vanilla import ListView, DetailView, CreateView


class LocationViewset(viewsets.ModelViewSet):
    serializer_class = LocationSerializer
    queryset = Location.objects.none()

    def get_queryset(self):
        community = self.request.GET.get('community',None)
        if community:
            return Location.objects.filter(community=community)
        name = self.request.GET.get('metro','')
        return Location.objects.filter(name__icontains=name)


# def addlocation(request):
#     if request.POST:
#         form = AddLocationForm(request.POST)
#         if form.is_valid():
#             s = Location(
#                 name=form.cleaned_data['name'],
#                 address=form.cleaned_data['address'],
#                 city_and_state=form.cleaned_data['city_and_state'],
#                 zip=form.cleaned_data['zip'],
#                 # what_kind=form.cleaned_data['what_kind'],
#                 latitude=form.cleaned_data['latitude'],
#                 longitude=form.cleaned_data['longitude'],
#             )
#
#             s.geom = GEOSGeometry('POINT(%s %s)' % (form.cleaned_data['longitude'], form.cleaned_data['latitude'],))
#             s.save()
#     else:
#         form = AddLocationForm()
#     makis = {}
#     for i in LocationType.objects.all():
#         makis[i.name] = i.maki_class
#
#     # makis = MAKI_CHOICES
#
#
#     return render(request, 'add.html', {'form': form,
#                                         'makis': makis})


class LocationList(ListView):
    model = Location


class LocationDetail(DetailView):
    model = Location


class LocationCreate(CreateView):
    model = Location
    form_class = AddLocationForm

    def form_valid(self, form):
        s = Location(
            name=form.cleaned_data['name'],
            address=form.cleaned_data['address'],
            city_and_state=form.cleaned_data['city_and_state'],
            zip=form.cleaned_data['zip'],
            # what_kind=form.cleaned_data['what_kind'],
            latitude=form.cleaned_data['latitude'],
            longitude=form.cleaned_data['longitude'],
            )

        s.geom = GEOSGeometry('POINT(%s %s)' % (form.cleaned_data['longitude'], form.cleaned_data['latitude'],))
        s.save()
        messages.info(self.request, '%s created.' % s.name)
        return redirect('addlocation')