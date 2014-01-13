from django.db import models
from thoughtbubble.models import ThoughtbubbleUser

COMMENT_LIVE = 'live'
COMMENT_FLAGGED = 'flagged'
COMMENT_PENDING = 'pending'

COMMENT_STATUSES = [
    (COMMENT_LIVE, 'Live'),
    (COMMENT_FLAGGED, 'Flagged'),
    (COMMENT_PENDING, 'Pending'),
]

class Comment(models.Model):
    user = models.ForeignKey(ThoughtbubbleUser)
    date_added = models.DateTimeField(default=None, null=True)
    date_edited = models.DateTimeField(default=None, null=True)
    comment = models.TextField(max_length=2048)
    status = models.CharField(max_length=10, choices=COMMENT_STATUSES, default=COMMENT_LIVE)
    parent = models.ForeignKey('self', null=True, blank=True, default=None, related_name="parent_comment")