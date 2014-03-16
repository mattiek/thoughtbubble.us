from django.shortcuts import render, get_object_or_404
from serializers import CitySerializer
from rest_framework import viewsets
from .models import Place

from ideation.idea.models import Idea
from django.contrib.gis.geos import Point
from django.contrib.gis.measure import D
from django.contrib.gis.geos import fromstr
from django.contrib.gis.geos import Polygon
from vanilla import DetailView, CreateView, UpdateView, ListView
from django.db.models import F, Q, Count
from geo.location.models import Location
from ideation.idea.forms import FilterForm, FOR_CHOICES_AND_EMPTY
from ideation.idea.models import IdeaType


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


class PlacesList(ListView):
    model = Place


class PlacesCreate(CreateView):
    model = Place


class PlacesDetail(DetailView):
    model = Place
    lookup_field = 'slug'
    lookup_url_kwarg = 'place'
    context_object_name = 'place'


    def get_object(self):
        """
        Custom object lookup that returns an instance based on both the
        'account' and 'slug' as provided in the URL keyword arguments.
        """
        queryset = self.get_queryset()
        place = self.kwargs['place']
        return get_object_or_404(queryset, slug__iexact=place)


    def get_context_data(self, **kwargs):
        context = super(PlacesDetail, self).get_context_data(**kwargs)
        locations = Location.objects.filter(organization__place= context['place'])
        ideas = Idea.objects.filter(Q(content_type__name='place', object_id=self.object.id) |
                                               Q(content_type__name='location', object_id__in=locations))


        ### Basic parameters
        self.organization = None
        self.place = None
        try:
            self.place = Place.objects.get(slug__iexact=self.kwargs.get('place', None))
            # self.organization = Organization.objects.get(slug__iexact=self.kwargs.get('organization', None))
        except:
            pass

        ### Ordering
        ordering = self.request.GET.get('order',None)
        if (ordering == 'support'):
            ideas = ideas.annotate(num_books=Count('ideasupport')).order_by('-num_books')
        else:
            ideas = ideas.order_by('-date_created')


        ### What
        what = self.request.GET.get('what',None)
        if what:
            ideas = ideas.filter(what_kind=what)


        ### When
        when = self.request.GET.get('when',None)
        if when and when.lower() != "when":
            ideas = ideas.filter(what_for=when)

        # ### Check to see that we are on an Organization Idea List page
        # if self.organization:
        #     organizations = Organization.objects.filter(slug__iexact=self.organization.slug).values_list('pk', flat=True)
        #
        #     ### Where
        #     where = self.request.GET.get('where_place',None)
        #     if where:
        #         wheres = Place.objects.filter(pk=where)
        #         qs = qs.filter(content_type__name='place', object_id__in=wheres)
        #     if not where:
        #         where = self.request.GET.get('where_location',None)
        #         if where:
        #             wheres = Location.objects.filter(pk=where)
        #         else:
        #             wheres = Location.objects.filter(organization= self.organization)#__pk=self.request.GET.get('org',None))
        #         qs = qs.filter(content_type__name='location', object_id__in=wheres)
        # else:
        #     pass

        context['ideas'] = ideas

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

        if self.organization:
            where_location = self.request.GET.get('where_location',None)
            # if where_location:
            f.fields['where_location'].initial = where_location
            f.fields['where_location'].queryset = Location.objects.filter(organization=self.organization)
            f.fields['where_location'].empty_label = self.organization.title

            # f.fields['org'].initial = self.organization.id
        else:
            f.fields['where_place'].queryset = Place.objects.filter()


        context['filterform'] = f


        ordering = self.request.GET.get('order',None)
        context['ordering'] = ordering

        return context

class PlacesUpdate(UpdateView):
    model = Place
    # success_url = reverse_lazy('organization_detail')

    # def get_success_url(self, *args, **kwargs):
    #     # super(UpdateView, self).get_success_url(*args, **kwargs)
    #     return reverse('organization_detail', kwargs=self.kwargs)

    def form_valid(self, form):
        s = super(PlacesUpdate,self).form_valid(form)
        return s