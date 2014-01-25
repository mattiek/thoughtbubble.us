from django.forms import widgets
from rest_framework import serializers
from models import City


class CitySerializer(serializers.HyperlinkedModelSerializer):
    properties = serializers.CharField(source='get_properties', read_only=True)
    center = serializers.CharField(source='get_center', read_only=True)
    type = serializers.CharField(source='get_type', read_only=True)

    class Meta:
        model = City
        fields = ('id', 'name', 'county', 'state_code', 'zip', 'latitude', 'longitude', 'type', 'properties', 'center')