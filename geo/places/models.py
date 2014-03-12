from django.contrib.gis.db import models
from django.contrib.gis.geos import Point
from model_utils.choices import Choices
from thoughtbubble.utils import url_safe

import json as JSON
from django.core.urlresolvers import reverse
from autoslug import AutoSlugField

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

    slug = AutoSlugField(populate_from='name', unique_with='state')

    def __unicode__(self):
        return "%s, %s" % (self.name, self.state_code)

    def save(self, *args, **kwargs):
        if not self.geom:
            self.geom = Point(self.longitude, self.latitude)
        super(Place, self).save(*args, **kwargs)


    def get_explore_link(self):
        return reverse('places_detail', args=[url_safe(self.name),])

    def add_idea_link(self):
        return reverse('addidea', args=[url_safe(self.name),])

    def get_absolute_url(self):
        return reverse('places_detail', args=[url_safe(self.name),])


    def get_geojson_type(self):
        return 'Feature'

    def get_center(self):
        return JSON.loads(self.geom.geojson)

    def get_properties(self):

        props = {}

        props['id'] = self.id
        props['explore'] = self.get_explore_link()
        props['title'] = self.name

        props['orgs'] = filter(lambda x: x, [x.get_center() for x in self.organization_set.all()])

        props['icon'] = {
            "iconUrl": "/static/images/map-point.png",
            "iconSize": [26, 33],
            "iconAnchor": [13, 30],
            "popupAnchor": [0, -25]
        }

        return props