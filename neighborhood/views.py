from models import Neighborhood
from serializers import NeighborhoodSerializer
from rest_framework import viewsets

class NeighborhoodViewset(viewsets.ModelViewSet):
    serializer_class = NeighborhoodSerializer
    queryset = Neighborhood.objects.none()

    def get_queryset(self):
        name = self.request.GET.get('city','')
        return Neighborhood.objects.filter(city__icontains=name)