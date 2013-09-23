from django.contrib.gis.db import models
from neighborhood.models import Neighborhood
from thoughtbubble.utils import path_and_rename
import json as JSON



class Community(models.Model):
    neighborhood = models.OneToOneField(Neighborhood)

    logo = models.ImageField(upload_to=path_and_rename('profiles', 'logo'), null=True, blank=True)

    title = models.CharField(max_length=255)
    website = models.URLField(max_length=255, null=True, blank=True)
    facebook_url = models.URLField(max_length=255, null=True, blank=True)
    twitter_url = models.URLField(max_length=255, null=True, blank=True)
    linkedin_url = models.URLField(max_length=255, null=True, blank=True)

    about = models.TextField(null=True, blank=True)



    class Meta:
        verbose_name_plural = "Communities"


class CommunityNews(models.Model):
    community = models.ForeignKey(Community)
    name = models.CharField(max_length=255, null=True, blank=True)
    img = models.ImageField(upload_to="communities/news", null=True, blank=True)
    content = models.TextField(null=True, blank=True)

    def __unicode__(self):
        return self.name
