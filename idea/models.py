from django.db import models
from neighborhood.models import Neighborhood
from thoughtbubble.utils import path_and_rename
from supportering.models import Support
from thoughtbubble.models import ThoughtbubbleUser
import os
import hashlib

FOR_CHOICES = [
    ('live', 'live'),
    ('work', 'work'),
    ('play', 'play'),
]


class IdeaType(models.Model):
    name = models.CharField(max_length=255)

    def __unicode__(self):
        return self.name


class Idea(models.Model):
    name = models.CharField(max_length=255)

    description = models.TextField()

    what_kind = models.ForeignKey(IdeaType)
    what_for = models.CharField(max_length=20, choices=FOR_CHOICES)
    where = models.ForeignKey(Neighborhood)

    user = models.ForeignKey(ThoughtbubbleUser, null=True)

    # support = models.ManyToManyField(Support)

    def __unicode__(self):
        return self.name

    def save(self, *args, **kwargs):
        super(Idea, self).save(*args, **kwargs)

    def get_title(self):
        return "%s in %s for %s" % (self.name, self.where, self.what_for)

    def comment_count(self):
        return 0

    def support_count(self):
        return 0



class IdeaImage(models.Model):
    idea = models.ForeignKey(Idea)
    img = models.ImageField(upload_to=path_and_rename('ideas','img'))
    name = models.CharField(max_length=255, blank=True, null=True)

    def __unicode__(self):
        if self.name:
            return self.name
        else:
            return 'Img'


class IdeaLink(models.Model):
    idea = models.ForeignKey(Idea)
    url = models.URLField()
    name = models.CharField(max_length=255, blank=True, null=True)

    def __unicode__(self):
        return self.url