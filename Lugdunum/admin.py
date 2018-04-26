from django.contrib import admin

from .models import OldPhoto, RecentPhoto, Place, Image

class ImageAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Image._meta.get_fields()]
admin.site.register(RecentPhoto)
admin.site.register(OldPhoto)
admin.site.register(Image, ImageAdmin)
admin.site.register(Place)