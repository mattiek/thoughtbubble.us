from django.forms import widgets
from rest_framework import serializers
from .models import Place, County, Region


class CitySerializer(serializers.HyperlinkedModelSerializer):
    properties = serializers.CharField(source='get_properties', read_only=True)
    center = serializers.CharField(source='get_center', read_only=True)
    type = serializers.CharField(source='get_geojson_type', read_only=True)

    class Meta:
        model = Place
        fields = ('id', 'name', 'county', 'state_code', 'zip_code', 'latitude', 'longitude', 'type', 'properties', 'center')


from import_export import resources


class CountyResource(resources.ModelResource):

    class Meta:
        model = County


class RegionResource(resources.ModelResource):

    class Meta:
        model = Region