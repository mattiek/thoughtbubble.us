from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from models import Location, LocationType, LocationNews, LocationImage
from serializers import LocationSerializer
from rest_framework import viewsets
from django.shortcuts import render, redirect, get_object_or_404
from forms import AddLocationForm, LocationUpdateForm
from django.contrib.gis.geos import GEOSGeometry
from django.contrib import messages
from geo.organization.models import Organization
from django.core.urlresolvers import reverse
from rest_framework import generics
from ideation.idea.models import Idea
from thoughtbubble.utils import url_safe


from partner.models import Partner

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

    def get_template_names(self):
        return self.request.device_template_dir + super(LocationList, self).get_template_names().pop()

from django.db.models import Q, Count
from ideation.idea.forms import FilterForm, FOR_CHOICES_AND_EMPTY
from ideation.idea.models import IdeaType

class LocationDetail(DetailView):
    model = Location
    lookup_field = 'slug'
    lookup_url_kwarg = 'location'

    def get_object(self):
        """
        Custom object lookup that returns an instance based on both the
        'account' and 'slug' as provided in the URL keyword arguments.
        """
        queryset = self.get_queryset()
        place = self.kwargs['place']
        org = self.kwargs['organization']
        location = self.kwargs['location']
        return get_object_or_404(queryset, organization__place__slug=place, organization__slug=org, slug=location)

    def get_ideas(self):

        id = self.kwargs.get('location',None)
        location = Location.objects.get(slug=id)
        ### Basic parameters
        qs = location.some_ideas.all()
        ### Ordering
        ordering = self.request.GET.get('order',None)
        if (ordering == 'support'):
            qs = qs.annotate(num_books=Count('ideasupport')).order_by('-num_books')
        else:
            qs = qs.order_by('-date_created')


        ### What
        what = self.request.GET.get('what',None)
        if what:
            qs = qs.filter(what_kind=what)


        ### When
        when = self.request.GET.get('when',None)
        if when and when.lower() != "when":
            qs = qs.filter(what_for=when)

                # else:
                #     locations = Location.objects.filter(organization__in=organizations)

                # return qs

        return qs

    def get_context_data(self, **kwargs):
        context = super(LocationDetail, self).get_context_data(**kwargs)

        id = self.kwargs.get('location',None)
        # if id:
        #     context['organization'] = Organization.objects.get(pk=id)
            # context['is_admin'] = self.request.user.is_admin
        location = Location.objects.get(slug=id)

        context['news_feed'] = LocationNews.objects.filter(location=location).order_by('-date_created')
        pics = LocationImage.objects.filter(location=location).order_by('ordering','-id').distinct('ordering')[:4]


        context['pictures'] = pics
        context['partners'] = location.partners.all()

        f = FilterForm()
        # f.fields['where'].initial = Location.objects.filter(organization=self.organization)
        what = self.request.GET.get('what',None)
        if what:
            f.fields['what'].initial = IdeaType.objects.get(pk=what)

        when = self.request.GET.get('when',None)
        if when:
            for i in FOR_CHOICES_AND_EMPTY:
                if i[0] == when:
                    f.fields['when'].initial = i[0]
                    # f.fields['when'].initial = FOR_CHOICES_AND_EMPTY[when]


        context['filterform'] = f


        ordering = self.request.GET.get('order',None)

        context['ideas'] = self.get_ideas()

        context['ordering'] = ordering
        return context

    def get_template_names(self):
        return self.request.device_template_dir + super(LocationDetail, self).get_template_names().pop()


class LocationUpdate(UpdateView):
    model = Location
    form_class = LocationUpdateForm
    lookup_field = 'slug'
    lookup_url_kwarg = 'location'

    def get_template_names(self):
        return self.request.device_template_dir + super(LocationUpdate, self).get_template_names().pop()

    def form_valid(self, form):
        comm = self.kwargs.get('location',None)
        s = Location.objects.get(slug=comm)
        s.name=form.cleaned_data['name']
        s.address=form.cleaned_data['address']
        s.city_and_state=form.cleaned_data['city_and_state']
        s.zip=form.cleaned_data['zip']
            # what_kind=form.cleaned_data['what_kind'],
        s.latitude=form.cleaned_data['latitude']
        s.longitude=form.cleaned_data['longitude']
        s.sherlock_description=form.cleaned_data['sherlock_description']

        s.about = form.cleaned_data['about']


        s.geom = GEOSGeometry('POINT(%s %s)' % (form.cleaned_data['longitude'], form.cleaned_data['latitude'],))

        pics = LocationImage.objects.filter(location=s).order_by('ordering','-id').distinct('ordering')[:4]

        pic1 = LocationImage(location=s,img=form.cleaned_data['pic1'], ordering=1)
        pic2 = LocationImage(location=s,img=form.cleaned_data['pic2'], ordering=2)
        pic3 = LocationImage(location=s,img=form.cleaned_data['pic3'], ordering=3)
        pic4 = LocationImage(location=s,img=form.cleaned_data['pic4'], ordering=4)

        pics = dict([(x.ordering, x) for x in pics])
        # TODO: More elegant

        prev_pic1 = pics.get(1,None)
        prev_pic2 = pics.get(2,None)
        prev_pic3 = pics.get(3,None)
        prev_pic4 = pics.get(4,None)
        if (pic1.img.name and not prev_pic1) or (pic1.img.name and pic1.img != prev_pic1.img):
            pic1.save()
        if (pic2.img.name and not prev_pic2) or (pic2.img.name and pic2.img != prev_pic2.img):
            pic2.save()
        if (pic3.img.name and not prev_pic3) or (pic3.img.name and pic3.img != prev_pic3.img):
            pic3.save()
        if (pic4.img.name and not prev_pic4) or (pic4.img.name and pic4.img != prev_pic4.img):
            pic4.save()

        s.save()
        messages.info(self.request, '%s updated.' % s.name)
        return redirect(s.get_update_url()
                        )

    def get_context_data(self, **kwargs):
        context = super(LocationUpdate, self).get_context_data(**kwargs)
        location = Location.objects.get(slug=self.kwargs['location'])
        context['action_url'] = location.get_update_url()
        context['organization'] = location.organization
        context['update'] = True
        if kwargs.get('id',None):
            self.form.fields['content_object'].initial = location
        return context


class LocationCreate(CreateView):
    model = Location
    form_class = AddLocationForm

    def get_template_names(self):
        return self.request.device_template_dir + super(LocationCreate, self).get_template_names().pop()

    def form_valid(self, form):
        comm = self.kwargs.get('organization',None)
        organization = Organization.objects.get(slug=comm)
        s = Location(
            name=form.cleaned_data['name'],
            address=form.cleaned_data['address'],
            city_and_state=form.cleaned_data['city_and_state'],
            zip=form.cleaned_data['zip'],
            # what_kind=form.cleaned_data['what_kind'],
            latitude=form.cleaned_data['latitude'],
            longitude=form.cleaned_data['longitude'],
            about=form.cleaned_data['about'],
            sherlock_description=form.cleaned_data['sherlock_description'],
            organization=organization
            )

        s.geom = GEOSGeometry('POINT(%s %s)' % (form.cleaned_data['longitude'], form.cleaned_data['latitude'],))
        s.save()

        pic1 = LocationImage(location=s,img=form.cleaned_data['pic1'])
        pic2 = LocationImage(location=s,img=form.cleaned_data['pic2'])
        pic3 = LocationImage(location=s,img=form.cleaned_data['pic3'])
        pic4 = LocationImage(location=s,img=form.cleaned_data['pic4'])
        # TODO: More elegant
        if pic1.img:
            pic1.save()
        if pic2.img:
            pic2.save()
        if pic3.img:
            pic3.save()
        if pic4.img:
            pic4.save()

        messages.info(self.request, '%s created.' % s.name)
        return redirect('location_update', s.organization.place.slug,
                        s.organization.slug,
                        s.slug,
                        )

    def get_context_data(self, **kwargs):
        context = super(LocationCreate, self).get_context_data(**kwargs)

        state = self.kwargs.get('state',None)
        city = self.kwargs.get('city',None)
        place = self.kwargs.get('place',None)
        comm = self.kwargs.get('organization',None)
        if comm:
            #TODO FIX THIS!
            organization = Organization.objects.get(place__slug=place, slug=comm)
            context['action_url'] = reverse('addlocation', args=[organization.place.slug, organization.slug,])
            context['organization'] = organization
            # self.form.fields['where'].initial = organization
        # context['is_admin'] = self.request.user.is_admin
        return context