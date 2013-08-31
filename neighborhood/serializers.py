from django.forms import widgets
from rest_framework import serializers
from models import Neighborhood


class NeighborhoodSerializer(serializers.HyperlinkedModelSerializer):
    center = serializers.CharField(source='getCenter', read_only=True)
    # geometry = serializers.CharField(source='getGeometry', read_only=True)
    # properties = serializers.CharField(source='getProperties', read_only=True)

    class Meta:
        model = Neighborhood
        fields = ('id', 'name', 'city', 'state', 'county', 'center')#, 'geometry', 'type', 'properties')