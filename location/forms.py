from django.contrib.gis import forms
from thoughtbubble.widgets import TypeAheadAdminWidget, SometimeWidget
from django.contrib.gis import admin
from floppyforms.widgets import RadioSelect
from models import Location

class LocationAdminForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(LocationAdminForm, self).__init__(*args, **kwargs)
        self.fields['city'].widget = TypeAheadAdminWidget()


class AddLocationForm(forms.ModelForm):
    news = forms.CharField(widget=forms.Textarea)
    news_picture1 = forms.ImageField()
    picture1 = forms.TextInput()

    class Meta:
        model = Location
        exclude = ['images','links',]
        widgets = {
            'name': forms.TextInput(attrs={'placeholder':'title'}),
            'address': forms.TextInput(attrs={'placeholder':'123 main st.'}),
            'city_and_state': forms.TextInput(attrs={'placeholder':'columbus, oh'}),
            'zip': forms.TextInput(attrs={'placeholder':'43201'}),
            # 'what_kind': SometimeWidget(choice=((1,'sfd'),(2,'dsfds'))),
            # 'what_kind': forms.Select(empty_label=None),
            'longitude': forms.TextInput(attrs={'placeholder':'39.958860'}),
            'latitude': forms.TextInput(attrs={'placeholder':'-82.998657'}),
        }
