from django.contrib.gis import forms
from models import Organization
from thoughtbubble.widgets import TypeAheadAdminWidget
from thoughtbubble.widgets import FilePicker

class OrganizationAdminForm(forms.ModelForm):
   # news = forms.CharField(max_length=255, widget=forms.Textarea(), required=False)

    def __init__(self, *args, **kwargs):
        super(OrganizationAdminForm, self).__init__(*args, **kwargs)
        # self.fields['city'].widget = TypeAheadAdminWidget()

    class Meta:
        model = Organization


class OrganizationUpdateForm(forms.ModelForm):
    # news = forms.CharField(max_length=255, widget=forms.Textarea(), required=False)

    def __init__(self, *args, **kwargs):
        super(OrganizationUpdateForm, self).__init__(*args, **kwargs)


    def is_valid(self):
        v = super(OrganizationUpdateForm, self).is_valid()
        return v

    def clean(self, *args, **kwargs):
        cleaned_data = super(OrganizationUpdateForm, self).clean()
        cleaned_data = dict(cleaned_data.items() + self.files.items())


        return cleaned_data

    class Meta:
        model = Organization
        fields = ['logo','title',
                  'website', 'facebook_url', 'twitter_url',
                  'linkedin_url', 'about', 'sherlock_description'
                  ]
        widgets = {
            'logo': FilePicker(),
            }