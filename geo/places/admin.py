from django.contrib.gis import admin
from .models import Place, County, Region
from import_export.admin import ImportExportModelAdmin
from .serializers import RegionResource, CountyResource
from django.contrib.gis import admin as geos_admin
from django.contrib.gis.geos import GEOSGeometry


class RegionAdmin(ImportExportModelAdmin):
    filter_horizontal = ['counties',]
    resource_class = RegionResource

class CountyAdmin(ImportExportModelAdmin):
    resource_class = CountyResource

class GoogleAdmin(geos_admin.OSMGeoAdmin):
    g = GEOSGeometry('POINT (9.191884 45.464254)') # Set map center
    g.set_srid(4326)
    g.transform(900913)
    default_lon = int(g.x)
    default_lat = int(g.y)
    default_zoom = 7
    extra_js = ["http://maps.google.com/maps/api/js?v=3.2&sensor=false"]
    map_template = 'gmgdav3.html'

admin.site.register(Place, GoogleAdmin)
admin.site.register(County,CountyAdmin)
admin.site.register(Region,RegionAdmin)