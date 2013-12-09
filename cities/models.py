from django.contrib.gis.db import models
from django.contrib.gis.geos import Point
import json as JSON

class City(models.Model):
    name = models.CharField(max_length=100)
    county = models.CharField(max_length=50)
    state = models.CharField(max_length=25)
    state_code = models.CharField(max_length=2)
    zip	= models.CharField(max_length=5)
    latitude = models.FloatField()
    longitude = models.FloatField()
    elevation = models.IntegerField()
    type = models.CharField(max_length=50)

    geom = models.PointField(null=True, blank=True)
    objects = models.GeoManager()


    def __unicode__(self):
        return "%s, %s" % (self.name, self.state_code,)

    def save(self, *args, **kwargs):
        if not self.geom:
            self.geom = Point(self.longitude, self.latitude)
        super(City, self).save(*args, **kwargs)


    def getType(self):
        return 'Feature'

    def getCenter(self):
        return JSON.loads(self.geom.geojson)

    def getProperties(self):

        props = {}

        #props['explore'] = reverse('neighborhood_detail', args=[str(self.state).lower(),str(self.city).lower(),str(self.id)])
        props['title'] = self.name

        if len(self.organization_set.all()):
            props['icon'] = {
                "iconUrl": "/static/images/featured-organization-location.png",
                "iconSize": [24, 30],
                "iconAnchor": [15, 22],
                "popupAnchor": [0, -25]
            }
        else:
            props['icon'] = {
                "iconUrl": "/static/images/map-point.png",
                "iconSize": [26, 33],
                "iconAnchor": [13, 30],
                "popupAnchor": [0, -25]
            }

        return props