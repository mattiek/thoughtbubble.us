from django.forms import widgets
from rest_framework import serializers
from models import City


class CitySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = City
        fields = ('id', 'name', 'county', 'state_code', 'zip', 'latitude', 'longitude')