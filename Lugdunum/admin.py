from django.contrib import admin

from .models import OldPhoto, RecentPhoto, Place


class PlaceAdmin(admin.ModelAdmin):
    list_display = ('id', 'description', 'latitude', 'longitude')


class OldPhotoAdmin(admin.ModelAdmin):
    list_display = [field.name for field in OldPhoto._meta.get_fields()]


class RecentPhotoAdmin(admin.ModelAdmin):
    list_display = [field.name for field in RecentPhoto._meta.get_fields()]


admin.site.register(RecentPhoto, RecentPhotoAdmin)
admin.site.register(OldPhoto, OldPhotoAdmin)
admin.site.register(Place, PlaceAdmin)
