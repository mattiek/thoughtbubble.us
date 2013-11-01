from django.forms import widgets
from rest_framework import serializers, pagination
from models import Community
from neighborhood.serializers import NeighborhoodSerializer


class FeatureSerializer(serializers.Serializer):

    his = '2323'
    def hi(self):
        return 'dsfsd'

    def __unicode__(self):
        return 'dsfsd'

class LinksSerializer(serializers.Serializer):
    next = pagination.NextPageField(source='*')
    prev = pagination.PreviousPageField(source='*')

class CustomPaginationSerializer(pagination.BasePaginationSerializer):
    links = LinksSerializer(source='*')  # Takes the page object as the source
    total_results = serializers.Field(source='paginator.count')
    pocus = serializers.Field(source='hi')
    # free = LinksSerializer(source='*')
    # something = serializers.Field(source='hi')
    results_field = 'features'


class CommunitySerializer(serializers.HyperlinkedModelSerializer):
    center = serializers.CharField(source='neighborhood.getCenter', read_only=True)
    geometry = serializers.CharField(source='neighborhood.getGeometry')
    properties = serializers.CharField(source='getProperties', read_only=True)
    type = serializers.CharField(source='neighborhood.getType', read_only=True)

    neighborhood = NeighborhoodSerializer()

    class Meta:
        model = Community
        fields = ('id', 'neighborhood', 'center', 'geometry', 'type', 'properties')

    @property
    def data(self):
        df = super(CommunitySerializer, self).data
        m = {
            "type": "FeatureCollection",
            "features": df,
        }
        return m