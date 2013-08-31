from django.contrib.gis import forms
from thoughtbubble.widgets import TypeAheadAdminWidget
from django.contrib.gis import admin

class LocationAdminForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(LocationAdminForm, self).__init__(*args, **kwargs)
        self.fields['city'].widget = TypeAheadAdminWidget()