from django.contrib.gis import admin
from models import Location, LocationImage, LocationNews, LocationType

class LocationAdmin(admin.OSMGeoAdmin):
    list_filter = ['city',]

admin.site.register(Location, LocationAdmin)
admin.site.register(LocationImage)
admin.site.register(LocationNews)
admin.site.register(LocationType)