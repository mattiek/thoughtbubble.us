from django.contrib.gis.db import models
from geo.places.models import Place
from thoughtbubble.utils import path_and_rename
# from thoughtbubble.models import ThoughtbubbleUser
import json as JSON
from django.core.urlresolvers import reverse

from partner.models import Partner
from thoughtbubble.utils import url_safe
from autoslug import AutoSlugField
import urllib
from django.conf import settings

from model_utils import Choices

class OrganizationCuratorRole(models.Model):
    title = models.CharField(max_length=30)
    authority = models.IntegerField(default=0)

    def __unicode__(self):
        return "%s" % self.title


class OrganizationCurator(models.Model):
    curator = models.ForeignKey(settings.AUTH_USER_MODEL)
    role = models.ForeignKey(OrganizationCuratorRole, null=True, blank=True)

    def __unicode__(self):
        s = "n/a"
        if self.role:
            s = self.role.title

        return "%s - %s" % (self.curator.username, s)


class Organization(models.Model):
    MOD_CHOICES = Choices('pending','active','rejected','disabled')
    status = models.CharField(max_length=20, choices=MOD_CHOICES, default=MOD_CHOICES.pending)
    place = models.ForeignKey(Place, null=True, blank=True)
    slug = AutoSlugField(populate_from='title', unique_with='place')

    logo = models.ImageField(upload_to=path_and_rename('profiles', 'logo'), null=True, blank=True)

    title = models.CharField(max_length=255)
    website = models.URLField(max_length=255, null=True, blank=True)
    facebook_url = models.URLField(max_length=255, null=True, blank=True)
    twitter_url = models.URLField(max_length=255, null=True, blank=True)
    linkedin_url = models.URLField(max_length=255, null=True, blank=True)


    about = models.TextField(null=True, blank=True)
    sherlock_description = models.TextField(null=True, blank=True)

    curators = models.ManyToManyField(OrganizationCurator, related_name="organization_curator", null=True, blank=True)

    members = models.ManyToManyField(settings.AUTH_USER_MODEL, null=True, blank=True)

    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)

    partners = models.ManyToManyField(Partner, null=True, blank=True)


    geom = models.MultiPolygonField(srid=4326, null=True, blank=True)
    objects = models.GeoManager()

    center = models.PointField(null=True, blank=True)

    class Meta:
        verbose_name_plural = "Organizations"

    def __unicode__(self):
        return "%s Organization" % self.title

    def get_description(self):
        return self.sherlock_description or 'no exploring descripton'

    def save(self, *args, **kwargs):
        if not self.center and self.geom:
            self.center = self.geom.centroid
        super(Organization, self).save(*args, **kwargs)

    def get_logo(self):
        if self.logo:
            return self.logo.url
        return ''

    def add_idea_url(self):
        if self.place:
            return reverse('addidea', args=[
                                        url_safe(self.place.slug),
                                        url_safe(self.slug),
        ])

    def list_ideas_url(self):
        if self.place:
            return reverse('idea_list', args=[
                                        url_safe(self.place.slug),
                                        url_safe(self.slug),

        ])

    def get_absolute_url(self):
        if self.place:
            return reverse('organization_detail', args=[url_safe(self.place.slug),url_safe(self.slug)])#args=[str(self.place.name.lower()), str(self.title.lower())])

    def get_update_url(self):
        if self.place:
            return reverse('organization_update', args=[url_safe(self.place.slug),url_safe(self.slug)])#args=[str(self.place.name.lower()), str(self.title.lower())])

    def get_join_url(self):
        if self.place:
            return reverse('organization_join', args=[url_safe(self.place.slug),url_safe(self.slug)])#args=[str(self.place.name.lower()), str(self.title.lower())])

    def get_pictures(self):
        return self.organizationimage_set.all()

    def get_id(self):
        return self.title.lower().replace(' ','-')

    def get_properties(self):

        props = {}

        props['explore'] = self.get_explore_link()
        props['title'] = self.title
        props['id'] = self.id
        props['icon'] = {
            "iconUrl": "/static/images/large-featured-location.png",
            # "iconSize": [47, 60],
            # "iconAnchor": [30, 44],
            "iconSize": [35, 45],
            "iconAnchor": [22, 33],
            "popupAnchor": [0, -25]
        }
        return props

    def get_locations_geojson(self):
        mapbox = [{ "geometry": {
            "type": "Point",
            "coordinates": [self.center[0], self.center[1]],
                },
                    "properties": {
                        "id": self.get_id(),
                        "zoom": 15
                    }
                  }]
        locations = self.location_set.all()

        for location in locations:
            latlng = [location.geom[0], location.geom[1]]

            geometry = { "geometry": {
                            "type": "Point",
                            "coordinates": latlng
                             },
                         "properties": {
                             "id": location.get_id(),
                             "zoom": 20
                         }
            }
            mapbox.append(geometry)

        return JSON.dumps(mapbox)

    def get_geometry(self):
        if self.geom:
            json = self.geom.geojson

            extent = self.geom.extent
            geojson = {}
            geojson['type'] = 'MultiPolygon'
            geojson['coordinates'] = [[[
                                           [extent[0], extent[1]],
                                           [extent[2], extent[1]],
                                           [extent[2], extent[3]],
                                           [extent[0], extent[3]],
                                           [extent[0], extent[1]],
                                           ]]]
            # return geojson
            return JSON.loads(json)


    def get_type(self):
        return 'Feature'

    def get_explore_link(self):
        if self.place:
            return reverse('sherlock', args=[url_safe(self.place.slug), url_safe(self.slug)])

    def get_center(self):
        if self.center:
            j = JSON.loads(self.center.geojson)
            d = {}
            d['geometry'] = j
            d['type'] = 'Feature'
            d['properties'] = {
                'title': self.title,
                'id': self.id,
                'explore': self.get_explore_link(),
                'icon': {
                "iconUrl": "/static/images/large-featured-location.png",
                "iconSize": [35, 45],
                "iconAnchor": [22, 33],
                "popupAnchor": [0, -25]
                }
            }
            return d

    # def sherlock(self):
    #     return ''

    def get_api_detail_url(self):
        if self.place:
            return reverse('organization_detail', args=[url_safe(self.place.slug),url_safe(self.slug)])#args=[str(self.place.name.lower()), str(self.title.lower())])


    def get_absolute_url(self):
        if self.place:
            return reverse('organization_detail', args=[url_safe(self.place.slug),url_safe(self.slug)])#args=[str(self.place.name.lower()), str(self.title.lower())])


    def get_location_add_url(self):
        if self.place:
            return reverse('addlocation', args=[url_safe(self.place.slug),url_safe(self.slug)])#args=[str(self.place.name.lower()), str(self.title.lower())])


    def get_extent(self):
        extent = self.geom.extent
        geojson = {}
        geojson['type'] = 'Polygon'
        geojson['coordinates'] = [
            [extent[0], extent[1]],
            [extent[2], extent[1]],
            [extent[2], extent[3]],
            [extent[0], extent[3]],
            [extent[0], extent[1]],
            ]
        return extent

    def get_fb_sharing(self):
        return {
            'share_copy': "Check out this organization.",
            'share_image': 'http://thoughtbubble.us/static/images/TB_socialicon.png',
            'share_caption': 'thoughtbubble.us',
            'share_name': "%s" % self.title,
            'share_link': 'http://thoughtbubble.us' + self.get_absolute_url(),
        }

    def get_twit_sharing(self):
        return {
            'text': "Check out %s on thoughtbubble.us! %s" % (self.title, 'http://thoughtbubble.us' + self.get_absolute_url())
        }

    def get_member__count(self):
        return self.members.count()


class OrganizationNews(models.Model):
    organization = models.ForeignKey(Organization)
    name = models.CharField(max_length=255, null=True, blank=True)
    img = models.ImageField(upload_to="organizations/news", null=True, blank=True)
    content = models.TextField(null=True, blank=True)

    class Meta:
        verbose_name_plural = "Organization News"

    def __unicode__(self):
        return self.name


class OrganizationImage(models.Model):
    organization = models.ForeignKey(Organization)
    img = models.ImageField(upload_to=path_and_rename('organizations','img'))
    name = models.CharField(max_length=255, blank=True, null=True)

    def __unicode__(self):
        if self.name:
            return self.name
        else:
            return 'Img'

