from django.db import models
from thoughtbubble.utils import path_and_rename
# from thoughtbubble.models import ThoughtbubbleUser
from django.conf import settings
import os
import hashlib
import datetime
from django.utils.timezone import now
from django.core.urlresolvers import reverse

from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic

from ideation.supportering.models import AbstractSupport

from thoughtbubble.utils import url_safe
from autoslug import AutoSlugField

from model_utils import Choices

import json as JSON

FOR_CHOICES = [
    ('morning', 'morning'),
    ('noon', 'noon'),
    ('night', 'night'),
    ('all day', 'all day'),
]


class IdeaType(models.Model):
    name = models.CharField(max_length=255)
    ordering = models.IntegerField(default=0)

    class Meta:
        ordering = ['ordering',]

    def __unicode__(self):
        return self.name



class Idea(models.Model):
    MOD_CHOICES = Choices('active','flagged','disabled')
    name = models.CharField(max_length=255)
    slug = AutoSlugField(populate_from='name',unique_with='object_id')

    description = models.TextField()

    what_kind = models.ForeignKey(IdeaType)
    what_for = models.CharField(max_length=20, choices=FOR_CHOICES)
    #where = models.ForeignKey(Location)

    # Getting Generic
    content_type = models.ForeignKey(ContentType, null=True)
    object_id = models.PositiveIntegerField()
    content_object = generic.GenericForeignKey()


    user = models.ForeignKey(settings.AUTH_USER_MODEL, null=True)

    date_created = models.DateTimeField(auto_now_add=True, default=now())
    date_modified = models.DateTimeField(auto_now=True, default=now())
    status = models.CharField(max_length=20, choices=MOD_CHOICES, default=MOD_CHOICES.active)

    # member = models.ForeignKey(ThoughtbubbleUser, related_name='member_idea_creator', null=True, blank=True)

    def __unicode__(self):
        return self.name

    def save(self, *args, **kwargs):
        super(Idea, self).save(*args, **kwargs)

    def get_title(self):
        return "%s in %s for %s" % (self.name, self.content_object, self.what_for)

    def comment_count(self):
        return 0

    def get_parent_title(self):
        if self.content_type.name == 'place':
            place = self.content_object
            return place.name
        else: # its a location
            location = self.content_object
            return location.organization.title

    def get_parent_label(self):
        if self.content_type.name == 'place':
            return "Place"
        else: # its a location
            return "Organization"

    def get_name(self):
        s = self.name
        indices = set([0])
        # s[0] = s[0].lower()
        return "".join(c.lower() if i in indices else c for i, c in enumerate(s))

    def get_parent_link(self):
        if self.content_type.name == 'place':
            place = self.content_object
            return reverse('places_detail',args=[
                           url_safe(place.slug) ])
        else: # its a location
            location = self.content_object
            return reverse('organization_detail',args=[
                         url_safe(location.organization.place.slug),
                         url_safe(location.organization.slug),
                          #  url_safe(location.slug)
            ])


    def support_count(self):
        return IdeaSupport.objects.filter(idea=self).count()

    def get_days_since_added(self):
        d = now() - self.date_created
        return d.days

    def get_add_to_location_url(self):
        if self.content_type.name == 'place':
            place = self.content_object
            return reverse('addidea',args=[
                url_safe(place.slug) ])
        else: # its a location
            location = self.content_object
            return reverse('addidea',args=[
                url_safe(location.organization.place.slug),
                url_safe(location.organization.slug),
                url_safe(location.slug),
                #  url_safe(location.slug)
            ])


    # TODO: Make these use place and location!
    def get_flag_url(self):
        return reverse('flag_idea',args=[url_safe(self.slug)])

    # TODO: Make these use place and location!
    def get_support_url(self):
        # if self.content_type.name == 'neighborhood':
        #     neighborhood = self.content_object
        # else: # its a location
        #     neighborhood = self.content_object.organization.neighborhood

        return reverse('support_idea',args=[url_safe(self.slug)])

    def get_absolute_url(self):
        if self.content_type.name == 'place':
            place = self.content_object
            return reverse('place_idea_detail', args=[
                url_safe(place.slug),
                url_safe(self.slug)])
        else: # its a location
            location = self.content_object
            return reverse('idea_detail', args=[
                                            url_safe(location.organization.place.slug),
                                            url_safe(location.organization.slug),
                                            url_safe(location.slug),
                                            url_safe(self.slug)])


    def get_idea_location_name(self):
        if self.content_type.name == 'place':
            place = self.content_object
            return place.name
        else: # its a location
            location = self.content_object
            return location.name

    def get_longitude(self):
        if self.content_type.name == 'place':
            place = self.content_object
            return place.get_center()['coordinates'][0]

        else: # its a location
            location = self.content_object
            return location.longitude

    def get_latitude(self):
        if self.content_type.name == 'place':
            place = self.content_object
            return place.get_center()['coordinates'][1]

        else: # its a location
            location = self.content_object
            return location.latitude


    def get_wants(self):
        who_wants = "I want"
        if self.support_count() > 1:
                who_wants = "We want"
        return who_wants

    def get_fb_sharing(self):
        who_wants = "I want"
        if self.support_count() > 1:
            who_wants = "We want"
        return {
            'share_copy': "Support my idea at thoughtbubble.us!",
            'share_image': 'http://thoughtbubble.us/static/images/TB_socialicon.png',
            'share_caption': 'thoughtbubble.us',
            'share_name': "%s %s in %s" % (who_wants, self.name, self.get_idea_location_name()),
            'share_link': 'http://thoughtbubble.us' + self.get_absolute_url(),
            }

    def get_linkedin_sharing(self):
        who_wants = "I want"
        if self.support_count() > 1:
            who_wants = "We want"
        return {
            'summary': "%s %s in %s. Let's make this happen!" % (who_wants, self.name, self.get_idea_location_name()),
            'title': "%s %s in %s" % (who_wants, self.name, self.get_idea_location_name()),
            'share_link': 'http://thoughtbubble.us' + self.get_absolute_url(),
            }

    def get_twit_sharing(self):
        who_wants = "I want"
        if self.support_count() > 1:
            who_wants = "We want"
        return {
            'text': "%s %s in %s. Let's make this happen! %s" % (who_wants, self.name, self.get_idea_location_name(), 'http://thoughtbubble.us' + self.get_absolute_url())
        }

    def get_properties(self):
        properties = {}
        properties['title'] = self.name
        # properties['marker-size'] = 'medium'
        # properties['marker-color'] = '#f0a'
        # properties['marker-symbol'] = self.what_kind.maki_class if self.what_kind else 'Z'
        properties['link'] = self.get_absolute_url()

        properties['icon'] = {
            "iconUrl": "/static/images/large-featured-location.png",
            "iconSize": [47, 60],
            "iconAnchor": [30, 44],
            "popupAnchor": [0, -25]
        }

        # properties['icon'] = {
        #     "iconUrl": "http://placekitten.com/50/50",
        #     "iconSize": [50, 50], # size of the icon
        #     "iconAnchor": [25, 25], # point of the icon which will correspond to marker's location
        #      "popupAnchor": [0, -25]  # point from which the popup should open relative to the iconAnchor
        # }
        return properties

    def get_properties_json(self):
        return JSON.dumps(self.get_properties())

class IdeaSupport(AbstractSupport):
    idea = models.ForeignKey(Idea)


class IdeaImage(models.Model):
    idea = models.ForeignKey(Idea)
    img = models.ImageField(upload_to=path_and_rename('ideas','img'))
    name = models.CharField(max_length=255, blank=True, null=True)
    ordering = models.IntegerField(default=0)
    active = models.BooleanField(default=False)


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