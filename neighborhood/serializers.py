from django.forms import widgets
from rest_framework import serializers, pagination
from models import Neighborhood


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


class NeighborhoodSerializer(serializers.ModelSerializer):
    center = serializers.CharField(source='getCenter', read_only=True)
    geometry = serializers.CharField(source='getGeometry')
    properties = serializers.CharField(source='getProperties', read_only=True)
    type = serializers.CharField(source='getType', read_only=True)

    class Meta:
        model = Neighborhood
        fields = ('id', 'name', 'city', 'state', 'county', 'center', 'geometry', 'type', 'properties', 'community')
        depth = 1 # Nested object

    @property
    def data(self):
        df = super(NeighborhoodSerializer, self).data
        if self.object:
            return df
        else:
            m = {
                "type": "FeatureCollection",
                "features": df,
            }
            return m


class NeighborhoodTypeaheadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Neighborhood
        fields = ('id', 'name', 'city', 'state', 'county', 'community')
        depth = 1 # Nested object