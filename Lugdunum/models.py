from django.db import models
from django.conf import settings
from django.utils import timezone
from Lugdunum_Server.settings import MEDIA_URL
from django.core.files import File
from django.dispatch import receiver
import os
import base64
class Place(models.Model):
    description = models.TextField(default="no_description")
    latitude = models.FloatField(default=0)
    longitude = models.FloatField(default=0)
    @classmethod
    def create(cls, latitude, longitude, description):
        place = cls(latitude = latitude, longitude=longitude, description=description)
        return place

class OldPhoto(models.Model):
    image = models.FileField(upload_to = MEDIA_URL, blank = True)
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
    @classmethod
    def create(cls, name, description, date, infoLink, file_string, place):
        oldphoto = cls(
            name=name,
            description=description,
            date=date,
            infoLink=infoLink,
            place=place
        )
        f = open(os.path.join(settings.MEDIA_ROOT,MEDIA_URL,name), 'wb+')
        myfile = File(f)
        img = base64.b64decode(file_string)
        myfile.write(img)
        oldphoto.image.save(name, myfile, save=False)
        return oldphoto

@receiver(models.signals.post_delete, sender=OldPhoto)
def auto_delete_file_on_delete(sender, instance, **kwargs):
    if instance.image:
        if os.path.isfile(instance.image.path):
            os.remove(instance.image.path)
class RecentPhoto(models.Model):
    image = models.FileField(upload_to = MEDIA_URL, blank = True)
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
