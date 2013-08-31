from django.db import models
from neighborhood.models import Neighborhood

FOR_CHOICES = (
    ('live', 'live'),
    ('work', 'work'),
    ('play', 'play'),
)


class IdeaType(models.Model):
    name = models.CharField(max_length=255)

    def __unicode__(self):
        return self.name


class IdeaImage(models.Model):
    img = models.ImageField(upload_to="ideas")
    name = models.CharField(max_length=255, blank=True, null=True)

    def __unicode__(self):
        return self.img


class IdeaLink(models.Model):
    url = models.URLField()
    name = models.CharField(max_length=255, blank=True, null=True)

    def __unicode__(self):
        return self.url


class Idea(models.Model):
    name = models.CharField(max_length=255)

    description = models.TextField()

    what_kind = models.ForeignKey(IdeaType)
    what_for = models.CharField(max_length=20, choices=FOR_CHOICES)
    where = models.ForeignKey(Neighborhood)

    images = models.ManyToManyField(IdeaImage)
    links = models.ManyToManyField(IdeaLink)

    def __unicode__(self):
        return self.name