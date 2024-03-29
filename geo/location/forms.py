from django.contrib.gis import forms
from thoughtbubble.widgets import TypeAheadAdminWidget, SometimeWidget
from django.contrib.gis import admin
from floppyforms.widgets import RadioSelect
from models import Location, LocationType, LocationImage
from thoughtbubble.widgets import FilePicker

class LocationAdminForm(forms.ModelForm):
    # news = forms.CharField(max_length=255, widget=forms.Textarea(), required=False)


    def __init__(self, *args, **kwargs):
        super(LocationAdminForm, self).__init__(*args, **kwargs)
        # self.fields['city'].widget = TypeAheadAdminWidget()
        self.fields['name'].widget =forms.TextInput(attrs={'placeholder': 'title'})
        self.fields['address'].widget =forms.TextInput(attrs={'placeholder': 'address'})
        self.fields['city_and_state'].widget =forms.TextInput(attrs={'placeholder': 'city and state'})
        self.fields['zip'].widget =forms.TextInput(attrs={'placeholder': 'zip code'})
        self.fields['latitude'].widget =forms.TextInput(attrs={'placeholder': 'latitude'})
        self.fields['longitude'].widget =forms.TextInput(attrs={'placeholder': 'longitude'})

    class Meta:
        model = Location



class LocationUpdateForm(forms.ModelForm):
    news = forms.CharField(max_length=255, widget=forms.Textarea(), required=False)

    pic1 = forms.ImageField(widget=FilePicker, required=False)
    pic2 = forms.ImageField(widget=FilePicker, required=False)
    pic3 = forms.ImageField(widget=FilePicker, required=False)
    pic4 = forms.ImageField(widget=FilePicker, required=False)

    def __init__(self, *args, **kwargs):
        super(LocationUpdateForm, self).__init__(*args, **kwargs)
        # self.fields['city'].widget = TypeAheadAdminWidget()
        self.fields['name'].widget =forms.TextInput(attrs={'placeholder': 'title'})
        self.fields['address'].widget =forms.TextInput(attrs={'placeholder': 'address'})
        self.fields['city_and_state'].widget =forms.TextInput(attrs={'placeholder': 'city and state'})
        self.fields['zip'].widget =forms.TextInput(attrs={'placeholder': 'zip code'})
        self.fields['latitude'].widget =forms.TextInput(attrs={'placeholder': 'latitude'})
        self.fields['longitude'].widget =forms.TextInput(attrs={'placeholder': 'longitude'})

        # Get the last 4 pics
        pics = LocationImage.objects.filter(location=self.instance).order_by('ordering','-id').distinct('ordering')[:4]
        for i,x in enumerate(pics):
            self.fields['pic%d' % (i + 1)].initial = x.img
            #self.fields['pic%d' % (i + 1)].initial = '<div class="cloak"><img src="%s"/></div>' % x.img.url

    def clean(self, *args, **kwargs):
        cleaned_data = super(LocationUpdateForm, self).clean()
        cleaned_data = dict(cleaned_data.items() + self.files.items())

        # name = cleaned_data.get("name")
        # address = cleaned_data.get("address")
        # city_and_state = cleaned_data.get("city_and_state")
        # zip = cleaned_data.get("zip")
        # latitude = cleaned_data.get("latitude")
        # longitude = cleaned_data.get("longitude")
        # # what_kind = cleaned_data.get("what_kind")
        # news = cleaned_data.get("news")
        # about = cleaned_data.get("about")
        # sherlock_description = cleaned_data.get("sherlock_description")
        # order = cleaned_data.get("order")

        return cleaned_data

    class Meta:
        model = Location


class AddLocationForm(forms.Form):

    name = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'placeholder': 'title'}),)
    address = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'placeholder': 'address'}), required=False)
    city_and_state = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'placeholder': 'city and state'}), required=False)
    zip = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'placeholder': 'zip code'}), required=False)
    # city = models.ForeignKey(City, null=True, blank=True)
    latitude = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'placeholder': 'latitude'}), required=False)
    longitude = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'placeholder': 'longitude'}), required=False)

    about = forms.CharField(max_length=255, widget=forms.Textarea(), required=False)
    sherlock_description = forms.CharField(max_length=255, widget=forms.Textarea(), required=False)
    news = forms.CharField(max_length=255, widget=forms.Textarea(), required=False)

    pic1 = forms.ImageField(widget=FilePicker, required=False)
    pic2 = forms.ImageField(widget=FilePicker, required=False)
    pic3 = forms.ImageField(widget=FilePicker, required=False)
    pic4 = forms.ImageField(widget=FilePicker, required=False)

    # what_kind = forms.ModelChoiceField(queryset=LocationType.objects.all(), empty_label=None, required=False)

    # geom = models.PointField(srid=4326, null=True, blank=True)
    # objects = models.GeoManager()

    def clean(self, *args, **kwargs):
        cleaned_data = super(AddLocationForm, self).clean()
        cleaned_data = dict(cleaned_data.items() + self.files.items())

        name = cleaned_data.get("name")
        address = cleaned_data.get("address")
        city_and_state = cleaned_data.get("city_and_state")
        zip = cleaned_data.get("zip")
        latitude = cleaned_data.get("latitude")
        longitude = cleaned_data.get("longitude")
        # what_kind = cleaned_data.get("what_kind")
        news = cleaned_data.get("news")
        about = cleaned_data.get("about")
        sherlock_description = cleaned_data.get("sherlock_description")

        return cleaned_data

    def __init__(self, *args, **kwargs):
        super(AddLocationForm, self).__init__(*args, **kwargs)



# class AddLocationSForm(forms.ModelForm):
#     # news = forms.CharField(widget=forms.Textarea)
#     # news_picture1 = forms.ImageField()
#     # picture1 = forms.TextInput()
#
#     class Meta:
#         model = Location
#         exclude = ['images','links',]
#         widgets = {
#             'name': forms.TextInput(attrs={'placeholder':'title'}),
#             'address': forms.TextInput(attrs={'placeholder':'123 main st.'}),
#             'city_and_state': forms.TextInput(attrs={'placeholder':'columbus, oh'}),
#             'zip': forms.TextInput(attrs={'placeholder':'43201'}),
#             # 'what_kind': SometimeWidget(choice=((1,'sfd'),(2,'dsfds'))),
#             # 'what_kind': forms.Select(empty_label=None),
#             'longitude': forms.TextInput(attrs={'placeholder':'39.958860'}),
#             'latitude': forms.TextInput(attrs={'placeholder':'-82.998657'}),
#         }
#
#     def clean(self, *args, **kwargs):
#         cleaned_data = super(AddLocationForm, self).clean()
#         a = 1
