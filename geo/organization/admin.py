from django.contrib.gis import admin

from models import Organization, OrganizationNews, OrganizationCurator, OrganizationCuratorRole, OrganizationImage
from forms import OrganizationAdminForm
import reversion

class OrganizationAdmin(reversion.VersionAdmin, admin.OSMGeoAdmin):
    form = OrganizationAdminForm
    filter_horizontal = ['curators', 'members', 'partners']
    list_display = ('title','place','order',)
    list_editable = ('order',)

    class Media:
        css = {
            "all": ("css/admin/location.css",)
        }
        js = ("js/jquery.js","js/plugins/typeahead.min.js","js/admin/location.js")

admin.site.register(Organization, OrganizationAdmin)
# admin.site.register(OrganizationNews)
admin.site.register(OrganizationCurator)
admin.site.register(OrganizationCuratorRole)
admin.site.register(OrganizationImage)
