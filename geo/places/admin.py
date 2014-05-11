from django.contrib.gis import admin
from .models import Place, County, Region
from import_export.admin import ImportExportModelAdmin
from .serializers import RegionResource, CountyResource


class RegionAdmin(ImportExportModelAdmin):
    filter_horizontal = ['counties',]
    resource_class = RegionResource

class CountyAdmin(ImportExportModelAdmin):
    resource_class = CountyResource

admin.site.register(Place)
admin.site.register(County,CountyAdmin)
admin.site.register(Region,RegionAdmin)