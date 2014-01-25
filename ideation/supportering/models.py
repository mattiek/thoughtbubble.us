from django.db import models
from thoughtbubble.settings import base
from thoughtbubble.models import ThoughtbubbleUser
from django.conf import settings
from threadedcomments.models import Comment


class AbstractSupport(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    date_created = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True


class CommentSupport(AbstractSupport):
    comment = models.ForeignKey(Comment)
