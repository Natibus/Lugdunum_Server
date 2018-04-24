from django.db import models
from django.conf import settings

class Photo(models.Model):
    image = models.FileField(upload_to=settings.MEDIA_ROOT, blank = True)
    name = models.TextField
    format = models.TextField
    class Meta:
        abstract = True

class Place(models.Model):
    description = models.TextField(null=True)
    latitude = models.FloatField(default=0)
    longitude = models.FloatField(default=0)
    
class OldPhoto(Photo):
    date = models.TextField
    description = models.TextField
    infoLink = models.TextField
    place = models.ForeignKey(
        Place,
        on_delete=models.CASCADE,
        null=True
        )

class RecentPhoto(Photo):
    date = models.DateTimeField
    note = models.FloatField
    noteNumber = models.IntegerField
    place = models.ForeignKey(
        Place,
        on_delete=models.CASCADE,
        null=True
        )
