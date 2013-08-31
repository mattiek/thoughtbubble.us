from django.forms import widgets
from rest_framework import serializers
from models import Location


class LocationSerializer(serializers.HyperlinkedModelSerializer):
    type = serializers.CharField(source='getFeature', read_only=True)
    geometry = serializers.CharField(source='getGeometry', read_only=True)
    properties = serializers.CharField(source='getProperties', read_only=True)

    class Meta:
        model = Location
        fields = ('id', 'name', 'geometry', 'type', 'properties')