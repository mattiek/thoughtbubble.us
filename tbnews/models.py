from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic

from django.core.urlresolvers import reverse

from model_utils.models import TimeStampedModel


class NewsItem(TimeStampedModel):

    # Getting Generic
    content_type = models.ForeignKey(ContentType, null=True)
    object_id = models.PositiveIntegerField()
    content_object = generic.GenericForeignKey()

    subject = models.CharField(max_length=255, null=True, blank=True)
    content = models.TextField(null=True, blank=True)

    img = models.ImageField(upload_to="news", null=True, blank=True)

    def __unicode__(self):
        return self.subject

    def update_url(self):
        return reverse('update_news_item', args=[self.id])

    class Meta:
        verbose_name_plural = "News Items"

