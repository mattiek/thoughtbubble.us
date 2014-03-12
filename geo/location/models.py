from django.contrib.gis.db import models
from geo.places.models import Place
import json as JSON
from django.contrib.gis.geos import GEOSGeometry
from geo.organization.models import Organization
from django.core.urlresolvers import reverse
from partner.models import Partner

from ideation.idea.models import Idea
from django.contrib.contenttypes import generic
from thoughtbubble.utils import url_safe
from autoslug import AutoSlugField

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


class Location(models.Model):
    name = models.CharField(max_length=255)
    slug = AutoSlugField(populate_from='name', unique_with='organization')
    address = models.CharField(max_length=255, null=True, blank=True)
    city_and_state = models.CharField(max_length=255, null=True, blank=True)
    zip = models.CharField(max_length=15, null=True, blank=True)
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)

    about = models.TextField(null=True, blank=True)
    sherlock_description = models.TextField(null=True, blank=True)

    what_kind = models.ForeignKey(LocationType, null=True, blank=True)

    geom = models.PointField(srid=4326, null=True, blank=True)
    objects = models.GeoManager()

    organization = models.ForeignKey(Organization, null=True, blank=True)

    partners = models.ManyToManyField(Partner, null=True, blank=True)

    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)

    some_ideas = generic.GenericRelation(Idea)


    def __unicode__(self):
        try:
            return "%s in %s" % (self.name,self.organization.title,)
        except:
            return "%s [no organization]" % (self.name,)

    def get_absolute_url(self):
        # state = 'oh'
        # city = 'columbus'
        # if self.organization:
        #     state = self.organization.neighborhood.state
        #     city = self.organization.neighborhood.city

        return reverse('location_detail',  args=[
            url_safe(self.organization.place.slug),
            url_safe(self.organization.slug),
            url_safe(self.slug)
        ])

    def get_id(self):
        return self.name.lower().replace(' ','-')

    def get_api_detail_url(self):
        return reverse('locations-detail', args=[
            url_safe(self.organization.place.slug),
            url_safe(self.organization.slug),
            url_safe(self.slug)
        ])

    def get_api_detail_url(self):
        return reverse('location_update', args=[
            url_safe(self.organization.place.slug),
            url_safe(self.organization.slug),
            url_safe(self.slug)
        ])

    def add_idea_url(self):
            return reverse('addidea', args=[
                                            url_safe(self.organization.place.slug),
                                            url_safe(self.organization.slug),
                                            url_safe(self.slug)
            ])

    def list_ideas_url(self):
        return reverse('idea_list', args=[url_safe(self.organization.place.slug),
                                          url_safe(self.organization.slug),
                                          url_safe(self.slug)
        ])

    def get_update_url(self):
        return reverse('location_update', args=[url_safe(self.organization.place.slug),
                                          url_safe(self.organization.slug),
                                          url_safe(self.slug)
        ])

    def get_description(self):
        return self.sherlock_description or 'no exploring descripton'

    def save(self, *args, **kwargs):
        # if not self.geom:
        self.geom = GEOSGeometry('POINT(%s %s)' % (self.longitude, self.latitude,))
        if self.geom:
            self.latitude = self.geom[1]
            self.longitude = self.geom[0]

        # Put in the correct Organization
        # s = Neighborhood.objects.filter(geom__contains=self.geom)
        # if s:
        #     self.organization = s[0]


        super(Location, self).save(*args, **kwargs)

    def get_geojson(self):
        return self.geom.geojson

    def get_geometry(self):
        return JSON.loads(self.geom.geojson)

    def get_feature(self):
        return 'Feature'

    def get_properties(self):
        properties = {}
        properties['title'] = self.name
        # properties['marker-size'] = 'medium'
        # properties['marker-color'] = '#f0a'
        # properties['marker-symbol'] = self.what_kind.maki_class if self.what_kind else 'Z'
        properties['link'] = self.get_absolute_url()

        properties['about'] = self.about

        properties['icon'] = {
            "iconUrl": "/static/images/large-featured-location.png",
            "iconSize": [47, 60],
            "iconAnchor": [30, 44],
            "popupAnchor": [0, -25]
        }

        # properties['icon'] = {
        #     "iconUrl": "http://placekitten.com/50/50",
        #     "iconSize": [50, 50], # size of the icon
        #     "iconAnchor": [25, 25], # point of the icon which will correspond to marker's location
        #      "popupAnchor": [0, -25]  # point from which the popup should open relative to the iconAnchor
        # }
        return properties

    @property
    def get_mapbox_json(self):
        mapbox = {}
        geometry = JSON.loads(self.get_geojson())
        mapbox['type'] = 'Feature'
        mapbox['geometry'] = geometry
        return mapbox


class LocationNews(models.Model):
    location = models.ForeignKey(Location)
    name = models.CharField(max_length=255, null=True, blank=True)
    img = models.ImageField(upload_to="news", null=True, blank=True)
    content = models.TextField(null=True, blank=True)

    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Location News"


class LocationImage(models.Model):
    location = models.ForeignKey(Location)
    img = models.ImageField(upload_to="locations")
    name = models.CharField(max_length=255, blank=True, null=True)

    def __unicode__(self):
        return self.name or "Image %d for %s" % (self.id, self.location,)
