from django.contrib.gis.db import models
import json as JSON

class Neighborhood(models.Model):
    state = models.CharField(max_length=2)
    county = models.CharField(max_length=43)
    city = models.CharField(max_length=64)
    name = models.CharField(max_length=64)
    regionid = models.FloatField()
    geom = models.MultiPolygonField(srid=4326)
    objects = models.GeoManager()

    center = models.PointField(null=True, blank=True)

    def __unicode__(self):
        return "%s - %s, %s" % (self.name,self.city,self.state,)

    def save(self, *args, **kwargs):
        self.center = self.geom.centroid
        super(Neighborhood, self).save(*args, **kwargs)

    def getCenter(self):
        return JSON.loads(self.center.geojson)

    def getGeometry(self):
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

    def getType(self):
        return 'Feature'

    def getProperties(self):
        return []

    def getExtent(self):
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




# Auto-generated `LayerMapping` dictionary for Neighborhood model
neighborhood_mapping = {
    'state' : 'STATE',
    'county' : 'COUNTY',
    'city' : 'CITY',
    'name' : 'NAME',
    'regionid' : 'REGIONID',
    'geom' : 'MULTIPOLYGON',
    }