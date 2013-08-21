from django.contrib.gis.db import models


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

    def __unicode__(self):
        return "%s, %s" % (self.name, self.state_code,)