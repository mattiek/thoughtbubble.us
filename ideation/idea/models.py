from django.db import models
from thoughtbubble.utils import path_and_rename
from thoughtbubble.models import ThoughtbubbleUser
#from location.models import Location
import os
import hashlib
import datetime
from django.utils.timezone import now
from django.core.urlresolvers import reverse

from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic

from ideation.supportering.models import AbstractSupport

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
    #where = models.ForeignKey(Location)

    # Getting Generic
    content_type = models.ForeignKey(ContentType, null=True)
    object_id = models.PositiveIntegerField()
    content_object = generic.GenericForeignKey()



    user = models.ForeignKey(ThoughtbubbleUser, null=True)

    date_created = models.DateTimeField(auto_now_add=True, default=now())
    date_modified = models.DateTimeField(auto_now=True, default=now())


    # member = models.ForeignKey(ThoughtbubbleUser, related_name='member_idea_creator', null=True, blank=True)

    def __unicode__(self):
        return self.name

    def save(self, *args, **kwargs):
        super(Idea, self).save(*args, **kwargs)

    def get_title(self):
        return "%s in %s for %s" % (self.name, self.content_object, self.what_for)

    def comment_count(self):
        return 0

    def support_count(self):
        return IdeaSupport.objects.filter(idea=self).count()

    def get_days_since_added(self):
        d = now() - self.date_created
        return d.days

    def get_support_url(self):
        # if self.content_type.name == 'neighborhood':
        #     neighborhood = self.content_object
        # else: # its a location
        #     neighborhood = self.content_object.organization.neighborhood

        return reverse('support_idea',args=[self.id])

    def get_absolute_url(self):
        # if self.content_type.name == 'neighborhood':
        #     neighborhood = self.content_object
        # else: # its a location
        #     neighborhood = self.content_object.organization.neighborhood

        return reverse('idea_detail', args=[
                                            self.content_object.name.lower(),
                                            self.content_object.name.lower(),
                                            self.id])

class IdeaSupport(AbstractSupport):
    idea = models.ForeignKey(Idea)


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
    url = models.CharField(max_length=1024)
    name = models.CharField(max_length=255, blank=True, null=True)

    def __unicode__(self):
        return self.url

    def save(self, *args, **kwargs):
        if not self.name:
            self.name = self.url
        return super(IdeaLink, self).save(*args, **kwargs)