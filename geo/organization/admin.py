from django.contrib.gis import admin

from models import Organization, OrganizationNews
from forms import OrganizationAdminForm
import reversion

class OrganizationAdmin(reversion.VersionAdmin, admin.OSMGeoAdmin):
    form = OrganizationAdminForm
    class Media:
        css = {
            "all": ("css/admin/location.css",)
        }
        js = ("js/jquery.js","js/plugins/typeahead.min.js","js/admin/location.js")

admin.site.register(Organization, OrganizationAdmin)
# admin.site.register(OrganizationNews)
