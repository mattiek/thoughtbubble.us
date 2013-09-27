from django.db import models
from thoughtbubble.settings import base
from thoughtbubble.models import ThoughtbubbleUser
from django.conf import settings


class AbstractSupport(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL)

    class Meta:
        abstract = True


