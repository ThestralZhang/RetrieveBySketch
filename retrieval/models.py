from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User


# Create your models here.

#
class Image(models.Model):
    path = models.CharField(max_length=100)
    tag1 = models.CharField(max_length=50, null=True, blank=True)
    tag2 = models.CharField(max_length=50, null=True, blank=True)
    tag3 = models.CharField(max_length=50, null=True, blank=True)
    uploaded_by = models.ForeignKey(User)
    uploaded_on = models.DateField()

    def __unicode__(self):
        return self.path


class LikeInfo(models.Model):
    image_path = models.ForeignKey(Image)
    liked_by = models.ForeignKey(User)

    def __unicode__(self):
        return self.id
