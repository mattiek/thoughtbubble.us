from django.contrib.gis.db import models
from django.contrib.gis.geos import Point


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