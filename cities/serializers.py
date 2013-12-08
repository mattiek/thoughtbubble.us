from django.forms import widgets
from rest_framework import serializers
from models import City


class CitySerializer(serializers.HyperlinkedModelSerializer):
    properties = serializers.CharField(source='getProperties', read_only=True)
    center = serializers.CharField(source='getCenter', read_only=True)
    type = serializers.CharField(source='getType', read_only=True)

    class Meta:
        model = City
        fields = ('id', 'name', 'county', 'state_code', 'zip', 'latitude', 'longitude', 'type', 'properties', 'center')