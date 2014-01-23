from django.forms import widgets
from rest_framework import serializers
from .models import Place


class CitySerializer(serializers.HyperlinkedModelSerializer):
    properties = serializers.CharField(source='getProperties', read_only=True)
    center = serializers.CharField(source='getCenter', read_only=True)
    type = serializers.CharField(source='get_geojson_type', read_only=True)

    class Meta:
        model = Place
        fields = ('id', 'name', 'county', 'state_code', 'zip_code', 'latitude', 'longitude', 'type', 'properties', 'center')