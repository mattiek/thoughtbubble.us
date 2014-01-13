from django.db import models
from ideation.idea.models import Idea
from thoughtbubble.models import ThoughtbubbleUser

class Project(models.Model):
    idea = models.ForeignKey(Idea)
    user = models.ForeignKey(ThoughtbubbleUser, null=True)
