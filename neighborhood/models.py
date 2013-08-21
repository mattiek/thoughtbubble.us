from django.contrib.gis.db import models

class Neighborhood(models.Model):
    state = models.CharField(max_length=2)
    county = models.CharField(max_length=43)
    city = models.CharField(max_length=64)
    name = models.CharField(max_length=64)
    regionid = models.FloatField()
    geom = models.MultiPolygonField(srid=4326)
    objects = models.GeoManager()

    def __unicode__(self):
        return "%s - %s, %s" % (self.name,self.city,self.state,)

# Auto-generated `LayerMapping` dictionary for Neighborhood model
neighborhood_mapping = {
    'state' : 'STATE',
    'county' : 'COUNTY',
    'city' : 'CITY',
    'name' : 'NAME',
    'regionid' : 'REGIONID',
    'geom' : 'MULTIPOLYGON',
    }