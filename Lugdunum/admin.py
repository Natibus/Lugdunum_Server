from django.contrib import admin

from .models import OldPhoto, RecentPhoto, Place

admin.site.register(RecentPhoto)
admin.site.register(OldPhoto)
admin.site.register(Place)