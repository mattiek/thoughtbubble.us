from models import Neighborhood
from serializers import NeighborhoodSerializer, NeighborhoodTypeaheadSerializer
from rest_framework import viewsets
from vanilla import DetailView, CreateView, UpdateView, ListView
from idea.models import Idea

class NeighborhoodViewset(viewsets.ModelViewSet):
    serializer_class = NeighborhoodSerializer
    queryset = Neighborhood.objects.none()
    paginate_by = None
    # pagination_serializer_class = CustomPaginationSerializer

    def get_queryset(self):
        name = self.request.GET.get('metro','')
        return Neighborhood.objects.filter(city__icontains=name, organization__isnull=True)


class NeighborhoodTypeaheadViewset(viewsets.ModelViewSet):
    serializer_class = NeighborhoodTypeaheadSerializer
    queryset = Neighborhood.objects.none()
    paginate_by = None

    def get_queryset(self):
        name = self.request.GET.get('metro','')
        neighborhood = self.request.GET.get('neighborhood','')
        max_results = self.request.GET.get('max','10')
        offset = self.request.GET.get('offset','0')
        return Neighborhood.objects.filter(name__icontains=neighborhood, city__icontains=name, organization__isnull=True)[offset:max_results]

class NeighborhoodDetail(DetailView):
    model = Neighborhood


    def get_context_data(self, **kwargs):
        context = super(NeighborhoodDetail, self).get_context_data(**kwargs)

        context['ideas'] = Idea.objects.filter(content_type__name='neighborhood', object_id=self.object.id)
        return context
