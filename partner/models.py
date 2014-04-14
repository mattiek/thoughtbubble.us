from django.db import models
from thoughtbubble.utils import path_and_rename

class Partner(models.Model):
    name = models.CharField(max_length=50, blank=True, null=True)
    img = models.ImageField(upload_to=path_and_rename('partner','img'))
    link = models.URLField(blank=True, null=True)

    def __unicode__(self):
        if self.name:
            return self.name
        return 'Partner Object'