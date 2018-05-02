from Lugdunum.models import Place, RecentPhoto, OldPhoto
from rest_framework import serializers
from django.db import models
from drf_extra_fields.fields import Base64ImageField
# Serializers define the API representation.


class PlaceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Place
        fields = ('id', 'description', 'latitude', 'longitude')

class OldPhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = OldPhoto
        fields= [field.name for field in OldPhoto._meta.get_fields()]

class RecentPhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = RecentPhoto
        fields = [field.name for field in RecentPhoto._meta.get_fields()]
