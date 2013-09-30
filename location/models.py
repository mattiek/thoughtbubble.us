from django.contrib.gis.db import models
from cities.models import City
import json as JSON
from django.contrib.gis.geos import GEOSGeometry
from community.models import Community
from neighborhood.models import Neighborhood
from django.core.urlresolvers import reverse

MAKI_CHOICES = (
    ('garden', 'Garden'),
    ('rocket', 'Rocket'),
    ('art-gallery', 'Art Gallery'),
    ('shop', 'shop'),
    ('fast-food', 'Fast Food'),
    ('bar', 'Bar'),
    ('grocery', 'Grocery'),
    ('cinema', 'Cinema'),
    ('baseball', 'Baseball'),
)
class LocationType(models.Model):
    name = models.CharField(max_length=255)
    maki_class = models.CharField(max_length=40, choices=MAKI_CHOICES, default="rocket")

    def __unicode__(self):
        return self.name


class LocationImage(models.Model):
    img = models.ImageField(upload_to="locations")
    name = models.CharField(max_length=255, blank=True, null=True)

    def __unicode__(self):
        return self.img


class LocationNews(models.Model):
    name = models.CharField(max_length=255, null=True, blank=True)
    img = models.ImageField(upload_to="news", null=True, blank=True)
    content = models.TextField(null=True, blank=True)

    def __unicode__(self):
        return self.name


class Location(models.Model):
    name = models.CharField(max_length=255)
    address = models.CharField(max_length=255, null=True, blank=True)
    city_and_state = models.CharField(max_length=255, null=True, blank=True)
    zip = models.CharField(max_length=15, null=True, blank=True)
    city = models.ForeignKey(City, null=True, blank=True)
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)

    about = models.TextField(null=True, blank=True)

    what_kind = models.ForeignKey(LocationType, null=True, blank=True)

    geom = models.PointField(srid=4326, null=True, blank=True)
    objects = models.GeoManager()

    community = models.ForeignKey(Neighborhood, null=True, blank=True)

    def __unicode__(self):
        return "%s - %s" % (self.name,self.city_and_state,)

    def get_absolute_url(self):
        return reverse('location_detail', args=[str(self.id)])


    def save(self, *args, **kwargs):
        if not self.geom:
            self.geom = GEOSGeometry('POINT(%s %s)' % (self.latitude, self.longitude,))
        if self.geom:
            self.latitude = self.geom[0]
            self.longitude = self.geom[1]

        # Put in the correct Community
        s = Neighborhood.objects.filter(geom__contains=self.geom)
        if s:
            self.community = s[0]


        super(Location, self).save(*args, **kwargs)

    def getGeoJSON(self):
        return self.geom.geojson

    def getGeometry(self):
        return JSON.loads(self.geom.geojson)

    def getFeature(self):
        return 'Feature'

    def getProperties(self):
        properties = {}
        properties['title'] = self.name
        properties['marker-size'] = 'medium'
        properties['marker-color'] = '#f0a'
        properties['marker-symbol'] = self.what_kind.maki_class if self.what_kind else 'Z'
        properties['link'] = self.get_absolute_url()

        # properties['icon'] = {
        #     "iconUrl": "http://placekitten.com/50/50",
        #     "iconSize": [50, 50], # size of the icon
        #     "iconAnchor": [25, 25], # point of the icon which will correspond to marker's location
        #      "popupAnchor": [0, -25]  # point from which the popup should open relative to the iconAnchor
        # }
        return properties

    @property
    def getMapboxJSON(self):
        mapbox = {}
        geometry = JSON.loads(self.getGeoJSON())
        mapbox['type'] = 'Feature'
        mapbox['geometry'] = geometry
        return mapbox




