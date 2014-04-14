from django.contrib.gis import admin
from models import Location, LocationImage, LocationNews, LocationType
from thoughtbubble.widgets import NullWidget, TypeAheadWidget
from django.forms.widgets import TextInput
from django.db import models
from forms import LocationAdminForm
import reversion

class LocationAdmin(reversion.VersionAdmin, admin.OSMGeoAdmin):
    form = LocationAdminForm
    list_display = ('name','organization','order',)
    list_editable = ('order',)
    list_filter = ('organization',)

    class Media:
        css = {
            "all": ("css/admin/location.css",)
        }
        js = ("js/jquery.js","js/plugins/typeahead.min.js","js/admin/location.js")


admin.site.register(Location, LocationAdmin)
admin.site.register(LocationImage)
admin.site.register(LocationNews)
admin.site.register(LocationType)