from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from models import Location, LocationType
from serializers import LocationSerializer
from rest_framework import viewsets
from django.shortcuts import render, redirect
from forms import AddLocationForm
from django.contrib.gis.geos import GEOSGeometry
from django.contrib import messages
from community.models import Community
from django.core.urlresolvers import reverse
from rest_framework import generics
from idea.models import Idea

from vanilla import ListView, DetailView, CreateView, UpdateView


class LocationViewset(viewsets.ModelViewSet):
    serializer_class = LocationSerializer
    queryset = Location.objects.none()

    def get_queryset(self):
        community = self.request.GET.get('community',None)
        if community:
            return Location.objects.filter(community=community)
        name = self.request.GET.get('metro','')
        return Location.objects.filter(name__icontains=name)



class LocationList(ListView):
    model = Location


class LocationDetail(DetailView):
    model = Location

    def get_context_data(self, **kwargs):
        context = super(LocationDetail, self).get_context_data(**kwargs)

        id = self.kwargs.get('pk',None)
        if id:
            context['community'] = Community.objects.get(pk=id)
            # context['is_admin'] = self.request.user.is_admin

        context['ideas'] = Idea.objects.filter(where=Location.objects.get(pk=self.kwargs['pk']))
        return context


class LocationUpdate(UpdateView):
    model = Location

    def get_context_data(self, **kwargs):
        context = super(LocationUpdate, self).get_context_data(**kwargs)
        context['action_url'] = reverse('location_update', args=[self.kwargs['pk'],])
        if kwargs.get('id',None):
            self.form.fields['where'].initial = Location.objects.get(pk=id)
            # context['is_admin'] = self.request.user.is_admin
        return context


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

    def get_context_data(self, **kwargs):
        context = super(LocationCreate, self).get_context_data(**kwargs)
        context['action_url'] = reverse('addlocation')
        if kwargs.get('id',None):
            self.form.fields['where'].initial = Location.objects.get(pk=id)
        # context['is_admin'] = self.request.user.is_admin
        return context