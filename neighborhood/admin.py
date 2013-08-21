from django.contrib.gis import admin
from models import Neighborhood

class NeighborhoodAdmin(admin.OSMGeoAdmin):
    list_filter = ['city',]

admin.site.register(Neighborhood, NeighborhoodAdmin)