from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from models import Location, LocationType, LocationNews, LocationImage
from serializers import LocationSerializer
from rest_framework import viewsets
from django.shortcuts import render, redirect
from forms import AddLocationForm, LocationAdminForm
from django.contrib.gis.geos import GEOSGeometry
from django.contrib import messages
from geo.organization.models import Organization
from django.core.urlresolvers import reverse
from rest_framework import generics
from ideation.idea.models import Idea
from thoughtbubble.utils import url_safe

from vanilla import ListView, DetailView, CreateView, UpdateView


class LocationViewset(viewsets.ModelViewSet):
    serializer_class = LocationSerializer
    queryset = Location.objects.none()

    def get_queryset(self):
        organization = self.request.GET.get('organization',None)
        if organization:
            return Location.objects.filter(organization=organization)
        name = self.request.GET.get('metro','')
        return Location.objects.filter(name__icontains=name)



class LocationList(ListView):
    model = Location


class LocationDetail(DetailView):
    model = Location
    lookup_field = 'slug'
    lookup_url_kwarg = 'location'

    def get_context_data(self, **kwargs):
        context = super(LocationDetail, self).get_context_data(**kwargs)

        id = self.kwargs.get('location',None)
        # if id:
        #     context['organization'] = Organization.objects.get(pk=id)
            # context['is_admin'] = self.request.user.is_admin
        location = Location.objects.get(slug=id)
        context['ideas'] = location.some_ideas.all() #Idea.objects.filter(content_object=location)
        context['news_feed'] = LocationNews.objects.filter(location=location).order_by('-date_created')
        context['pictures'] = LocationImage.objects.filter(location=location).order_by('-date_created')
        return context


class LocationUpdate(UpdateView):
    model = Location
    form_class = LocationAdminForm

    def form_valid(self, form):
        comm = self.kwargs.get('pk',None)
        s = Location.objects.get(pk=comm)
        s.name=form.cleaned_data['name']
        s.address=form.cleaned_data['address']
        s.city_and_state=form.cleaned_data['city_and_state']
        s.zip=form.cleaned_data['zip']
            # what_kind=form.cleaned_data['what_kind'],
        s.latitude=form.cleaned_data['latitude']
        s.longitude=form.cleaned_data['longitude']

        s.about = form.cleaned_data['about']


        s.geom = GEOSGeometry('POINT(%s %s)' % (form.cleaned_data['longitude'], form.cleaned_data['latitude'],))
        s.save()
        messages.info(self.request, '%s updated.' % s.name)
        return redirect('location_update', self.kwargs.get('state'),
                        self.kwargs.get('city'),
                        self.kwargs.get('pk'),
                        )

    def get_context_data(self, **kwargs):
        context = super(LocationUpdate, self).get_context_data(**kwargs)
        location = Location.objects.get(pk=self.kwargs['pk'])
        context['action_url'] = reverse('location_update',
                                        args=[self.kwargs['pk'],])
        context['organization'] = location.organization
        context['update'] = True
        if kwargs.get('id',None):
            self.form.fields['content_object'].initial = location
        return context


class LocationCreate(CreateView):
    model = Location
    form_class = AddLocationForm

    def form_valid(self, form):
        comm = self.kwargs.get('organization',None)
        organization = Organization.objects.get(pk=comm)
        s = Location(
            name=form.cleaned_data['name'],
            address=form.cleaned_data['address'],
            city_and_state=form.cleaned_data['city_and_state'],
            zip=form.cleaned_data['zip'],
            # what_kind=form.cleaned_data['what_kind'],
            latitude=form.cleaned_data['latitude'],
            longitude=form.cleaned_data['longitude'],
            organization=organization
            )

        s.geom = GEOSGeometry('POINT(%s %s)' % (form.cleaned_data['longitude'], form.cleaned_data['latitude'],))
        s.save()
        messages.info(self.request, '%s created.' % s.name)
        return redirect('location_update', self.kwargs.get('state'),
                        self.kwargs.get('city'),
                        s.id,
                        )

    def get_context_data(self, **kwargs):
        context = super(LocationCreate, self).get_context_data(**kwargs)

        state = self.kwargs.get('state',None)
        city = self.kwargs.get('city',None)
        comm = self.kwargs.get('organization',None)
        if comm:
            organization = Organization.objects.get(pk=comm)
            context['action_url'] = reverse('addlocation', args=[url_safe(comm.slug),])
            context['organization'] = organization
            # self.form.fields['where'].initial = organization
        # context['is_admin'] = self.request.user.is_admin
        return context