from models import Neighborhood
from serializers import NeighborhoodSerializer, CustomPaginationSerializer
from rest_framework import viewsets

class NeighborhoodViewset(viewsets.ModelViewSet):
    serializer_class = NeighborhoodSerializer
    queryset = Neighborhood.objects.none()
    paginate_by = None
    # pagination_serializer_class = CustomPaginationSerializer

    def get_queryset(self):
        name = self.request.GET.get('metro','')
        return Neighborhood.objects.filter(city__icontains=name, community__isnull=True)