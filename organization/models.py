from django.contrib.gis.db import models
from neighborhood.models import Neighborhood
from thoughtbubble.utils import path_and_rename
from thoughtbubble.models import ThoughtbubbleUser
import json as JSON
from django.core.urlresolvers import reverse

from partner.models import Partner


class Organization(models.Model):
    neighborhood = models.OneToOneField(Neighborhood)

    logo = models.ImageField(upload_to=path_and_rename('profiles', 'logo'), null=True, blank=True)

    title = models.CharField(max_length=255)
    website = models.URLField(max_length=255, null=True, blank=True)
    facebook_url = models.URLField(max_length=255, null=True, blank=True)
    twitter_url = models.URLField(max_length=255, null=True, blank=True)
    linkedin_url = models.URLField(max_length=255, null=True, blank=True)

    about = models.TextField(null=True, blank=True)

    curator = models.ForeignKey(ThoughtbubbleUser, related_name="organization_curator", null=True, blank=True)

    members = models.ManyToManyField(ThoughtbubbleUser, null=True, blank=True)

    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)

    partners = models.ManyToManyField(Partner, null=True, blank=True)

    class Meta:
        verbose_name_plural = "Organizations"

    def __unicode__(self):
        return "%s Organization" % self.title

    def get_logo(self):
        if self.logo:
            return self.logo.url
        return ''

    def get_absolute_url(self):
        return reverse('organization_detail', args=[str(self.neighborhood.state).lower(),str(self.neighborhood.city).lower(),str(self.id)])

    def get_pictures(self):
        return self.organizationimage_set.all()

    def get_id(self):
        return self.title.lower().replace(' ','-')

    def getProperties(self):

        props = {}

        props['explore'] = reverse('sherlock', args=[str(self.neighborhood.state).lower(),str(self.neighborhood.city).lower(),str(self.id)])
        props['title'] = self.title
        props['icon'] = {
            "iconUrl": "/static/images/featured-organization-location.png",
            "iconSize": [24, 30],
            "iconAnchor": [15, 22],
            "popupAnchor": [0, -25]
        }
        return props

    def getLocationsGeoJSON(self):
        mapbox = [{ "geometry": {
            "type": "Point",
            "coordinates": [self.neighborhood.center[0], self.neighborhood.center[1]],
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

