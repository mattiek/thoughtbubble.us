from django.db import models
from thoughtbubble.settings import base
from thoughtbubble.models import ThoughtbubbleUser

class Support(models.Model):
    user = models.ForeignKey(ThoughtbubbleUser)