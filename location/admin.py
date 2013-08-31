from django.contrib.gis import admin
from models import Location, LocationImage, LocationNews, LocationType
from thoughtbubble.widgets import NullWidget
from django.db import models

class LocationAdmin(admin.OSMGeoAdmin):
    formfield_overrides = {
        models.ForeignKey: {'widget': NullWidget},
        }

admin.site.register(Location, LocationAdmin)
admin.site.register(LocationImage)
admin.site.register(LocationNews)
admin.site.register(LocationType)