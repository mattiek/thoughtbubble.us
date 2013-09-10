from django.db import models
from neighborhood.models import Neighborhood
from thoughtbubble.utils import md5_for_file
from supportering.models import Support
import os
import hashlib

FOR_CHOICES = [
    ('live', 'live'),
    ('work', 'work'),
    ('play', 'play'),
]


def path_and_rename(path):
    def wrapper(instance, filename):
        ext = filename.split('.')[-1]
        chunks = instance.img.chunks()
        md5 = hashlib.md5()
        for data in chunks:
            if not data:
                break
            md5.update(data)

        return os.path.join(path, "{}.{}".format(md5.hexdigest(),ext))
    return wrapper


class IdeaType(models.Model):
    name = models.CharField(max_length=255)

    def __unicode__(self):
        return self.name


class IdeaImage(models.Model):
    img = models.ImageField(upload_to=path_and_rename('sli'))
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

    support = models.ManyToManyField(Support)

    def __unicode__(self):
        return self.name

    def save(self, *args, **kwargs):
        super(Idea, self).save(*args, **kwargs)
