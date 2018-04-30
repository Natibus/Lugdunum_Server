from Lugdunum.models import Place, RecentPhoto, Image, OldPhoto
from rest_framework import serializers
from django.db import models
from drf_extra_fields.fields import Base64ImageField
# Serializers define the API representation.


class PlaceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Place
        fields = ('description', 'latitude', 'longitude')

class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model=Image
        fields=[field.name for field in Image._meta.get_fields()]

class OldPhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model=OldPhoto
        fields=('name', 'format', 'image', 'pk')
class RecentPhotoSerializer(serializers.ModelSerializer):
    
    class Meta:
        # name = models.TextField()
        model = RecentPhoto
        name = models.TextField()
        fields = ('name',)
