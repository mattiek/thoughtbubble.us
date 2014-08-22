from django.forms import widgets
from rest_framework import serializers, pagination
from models import Organization


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


class OrganizationSerializer(serializers.HyperlinkedModelSerializer):
    center = serializers.CharField(source='get_center', read_only=True)
    # geometry = serializers.CharField(source='get_geometry')
    properties = serializers.CharField(source='get_properties', read_only=True)
    type = serializers.CharField(source='get_type', read_only=True)

    class Meta:
        model = Organization
        # fields = ('id', 'place', 'center', 'geometry', 'type', 'properties')
        fields = ('id', 'place', 'center', 'type', 'properties')

    @property
    def data(self):
        df = super(OrganizationSerializer, self).data
        m = {
            "type": "FeatureCollection",
            "features": df,
        }
        return m