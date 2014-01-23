from django.contrib.gis import forms
from models import Organization
from thoughtbubble.widgets import TypeAheadAdminWidget

class OrganizationAdminForm(forms.ModelForm):
    news = forms.CharField(max_length=255, widget=forms.Textarea(), required=False)

    def __init__(self, *args, **kwargs):
        super(OrganizationAdminForm, self).__init__(*args, **kwargs)
        # self.fields['city'].widget = TypeAheadAdminWidget()

    class Meta:
        model = Organization

