from django.contrib.gis.db import models
from django.contrib.gis.geos import Point
from model_utils.choices import Choices

import json as JSON
from django.core.urlresolvers import reverse

class Place(models.Model):
    REGIONS = Choices(
        'northwest',
        'northeast',
        'southeast',
        'southwest',
        'western',
        'central',
    )

    name = models.CharField(max_length=255)
    county = models.CharField(max_length=255, null=True, blank=True)
    state = models.CharField(max_length=255, null=True, blank=True)
    state_code = models.CharField(max_length=255, null=True, blank=True)
    zip_code = models.IntegerField()
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    elevation = models.IntegerField(default=0)
    place_type = models.CharField(max_length=255, null=True, blank=True)
    population= models.IntegerField(default=0)

    region = models.CharField(max_length=255, choices=REGIONS, default=REGIONS.central)

    geom = models.PointField(srid=4326, null=True, blank=True)
    objects = models.GeoManager()

    def __unicode__(self):
        return "%s, %s" % (self.name, self.state_code)

    def save(self, *args, **kwargs):
        if not self.geom:
            self.geom = Point(self.longitude, self.latitude)
        super(Place, self).save(*args, **kwargs)

    def get_geojson_type(self):
        return 'Feature'

    def getCenter(self):
        return JSON.loads(self.geom.geojson)

    def getProperties(self):

        props = {}

        props['id'] = self.id
        props['explore'] = ''#reverse('city_detail', args=[str(self.id)])
        props['title'] = self.name

        props['orgs'] = [x.getCenter() for x in self.organization_set.all()]

        props['icon'] = {
            "iconUrl": "/static/images/map-point.png",
            "iconSize": [26, 33],
            "iconAnchor": [13, 30],
            "popupAnchor": [0, -25]
        }

        return props