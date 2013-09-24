from models import Community
from serializers import CommunitySerializer, CustomPaginationSerializer
from rest_framework import viewsets

class CommunityViewset(viewsets.ModelViewSet):
    serializer_class = CommunitySerializer
    queryset = Community.objects.none()
    paginate_by = None
    # pagination_serializer_class = CustomPaginationSerializer

    def get_queryset(self):
        name = self.request.GET.get('city','')
        return Community.objects.filter(neighborhood__city__icontains=name)