from django.contrib.gis import admin
from models import Location, LocationImage, LocationNews, LocationType
from thoughtbubble.widgets import NullWidget, TypeAheadWidget
from django.forms.widgets import TextInput
from django.db import models
from forms import LocationAdminForm

class LocationAdmin(admin.OSMGeoAdmin):
    form = LocationAdminForm

    class Media:
        css = {
            "all": ("css/admin/location.css",)
        }
        js = ("js/jquery.js","js/plugins/typeahead.min.js","js/admin/location.js")


admin.site.register(Location, LocationAdmin)
admin.site.register(LocationImage)
admin.site.register(LocationNews)
admin.site.register(LocationType)