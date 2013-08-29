from django.contrib.gis.db import models
from cities.models import City

class LocationType(models.Model):
    name = models.CharField(max_length=255)

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

    what_kind = models.ForeignKey(LocationType)

    # geom = models.MultiPolygonField(srid=4326)
    objects = models.GeoManager()

    def __unicode__(self):
        return "%s - %s" % (self.name,self.city_and_state,)
