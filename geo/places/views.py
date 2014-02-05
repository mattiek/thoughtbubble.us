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
    lookup_field = 'name'
    lookup_url_kwarg = 'place'
    context_object_name = 'place'


    def get_object(self):
        """
        Custom object lookup that returns an instance based on both the
        'account' and 'slug' as provided in the URL keyword arguments.
        """
        queryset = self.get_queryset()
        place = self.kwargs['place']
        return get_object_or_404(queryset, name__iexact=place)


    def get_context_data(self, **kwargs):
        context = super(PlacesDetail, self).get_context_data(**kwargs)
        context['ideas'] = Idea.objects.filter(content_type__name='place', object_id=self.object.id)
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