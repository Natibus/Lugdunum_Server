from django.db import models
from django.conf import settings
from django.utils import timezone

class Place(models.Model):
    description = models.TextField(null=True)
    latitude = models.FloatField(default=0)
    longitude = models.FloatField(default=0)
    
class OldPhoto(models.Model):
    image = models.ImageField(upload_to=settings.MEDIA_ROOT, blank = True)
    name = models.TextField(default="default_name")
    format = models.TextField(default="unknown")
    date = models.TextField(default="unknown")
    description = models.TextField(default="no description")
    infoLink = models.TextField(default="no infolink")
    place = models.ForeignKey(
        Place,
        on_delete=models.CASCADE,
        null=True
        )

class RecentPhoto(models.Model):
    image = models.ImageField(upload_to=settings.MEDIA_ROOT, blank = True)
    name = models.TextField(default="default_name")
    format = models.TextField(default="unknown")
    date = models.DateTimeField(blank=True, default=timezone.now())
    note = models.FloatField(blank=True, default=0)
    noteNumber = models.IntegerField(default=0)
    place = models.ForeignKey(
        Place,
        on_delete=models.CASCADE,
        null=True
        )

class Image(models.Model):
    image = models.ImageField(upload_to=settings.MEDIA_ROOT, blank = True)
    name = models.TextField(default="default_name")
    format = models.TextField(default="unknown")