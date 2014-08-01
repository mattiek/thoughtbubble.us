from django.contrib.gis.db import models
from django.contrib.gis.geos import Point
from model_utils.choices import Choices
from thoughtbubble.utils import url_safe

import json as JSON
from django.core.urlresolvers import reverse
from autoslug import AutoSlugField

from ideation.idea.models import Idea

class County(models.Model):
    name = models.CharField(max_length=255, null=True, blank=True)
    state_code = models.CharField(max_length=255, null=True, blank=True)

    class Meta:
        verbose_name_plural = "Counties"
        ordering = ['name',]

    def __unicode__(self):
        return "%s, %s" % (self.name, self.state_code,)


class Region(models.Model):
    name = models.CharField(max_length=255, null=True, blank=True)
    capital = models.ForeignKey('Place', null=True, blank=True)
    counties = models.ManyToManyField(County)

    def __unicode__(self):
        return "%s Region" % self.name


class Place(models.Model):
    name = models.CharField(max_length=255)
    county = models.CharField(max_length=255, null=True, blank=True)
    county_fk = models.ForeignKey(County,  null=True)
    state = models.CharField(max_length=255, null=True, blank=True)
    state_code = models.CharField(max_length=255, null=True, blank=True)
    zip_code = models.IntegerField()
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    elevation = models.IntegerField(default=0, null=True, blank=True)
    place_type = models.CharField(max_length=255, null=True, blank=True)
    population= models.IntegerField(default=0, null=True, blank=True)

    #TODO: classification = models.IntegerField City or Neighborhood
    #TODO: Add DEBUG HEADER to see what IP you have and the region detect

    geom = models.PointField(srid=4326, null=True, blank=True)
    objects = models.GeoManager()

    slug = AutoSlugField(populate_from='name', unique_with='state')

    class Meta:
        ordering = ['name',]

    def __unicode__(self):
        return "%s, %s" % (self.name, self.state_code)

    def save(self, *args, **kwargs):
        super(Place, self).save(*args, **kwargs)

        if not self.geom and self.longitude and self.latitude:
            self.geom = Point(self.longitude, self.latitude)

        # if not self.county_fk:
        #     c = County.objects.get_or_create(name=self.county, state_code=self.state_code)[0]
        #     self.county_fk = c




    def get_explore_link(self):
        return reverse('places_detail', args=[url_safe(self.slug),])

    def add_idea_link(self):
        return reverse('addidea', args=[url_safe(self.slug),])

    def get_absolute_url(self):
        return reverse('places_detail', args=[url_safe(self.slug),])


    def get_number_ideas(self):
        return Idea.objects.filter(object_id=self.id, content_type__name__iexact='place').count()

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


    def get_linkedin_sharing(self):
        return {
            'summary': "Check out this place!",
            'title': "%s" % self.name,
            'share_link': 'http://thoughtbubble.us' + self.get_absolute_url(),
            }

    def get_fb_sharing(self):
        return {
            'share_copy': "Check out this place!",
            'share_image': 'http://thoughtbubble.us/static/images/TB_socialicon.png',
            'share_caption': 'thoughtbubble.us',
            'share_name': "%s" % self.name,
            'share_link': 'http://thoughtbubble.us' + self.get_absolute_url(),
            }

    def get_twit_sharing(self):
        return {
            'text': "Check out %s on thoughtbubble.us! %s" % (self.name, 'http://thoughtbubble.us' + self.get_absolute_url())
        }