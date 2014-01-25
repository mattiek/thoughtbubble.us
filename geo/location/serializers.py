from django.forms import widgets
from rest_framework import serializers
from models import Location


class LocationSerializer(serializers.HyperlinkedModelSerializer):
    type = serializers.CharField(source='get_feature', read_only=True)
    geometry = serializers.CharField(source='get_geometry', read_only=True)
    properties = serializers.CharField(source='get_properties', read_only=True)

    results_field = 'features'

    class Meta:
        model = Location
        fields = ('id', 'name', 'geometry', 'type', 'properties')


    # @property
    # def data(self):
    #     df = super(LocationSerializer, self).data
    #     if self.object:
    #         return df
    #     else:
    #         m = {
    #             "type": "FeatureCollection",
    #             "features": df,
    #             }
    #         return m