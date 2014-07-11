# -*- coding: utf-8 -*-
from django import forms
from django.forms import ModelForm
from models import *
from thoughtbubble.widgets import FilePicker
from geo.location.models import Location
from geo.places.models import Place


FOR_CHOICES_AND_EMPTY = [('when','when')] + FOR_CHOICES
REFINE_CHOICES = [('refine','refine'), ('recent','recent'), ('support','most supported')]
# <select name="order" id="order">
# <option value="">refine</option>
# <option value="recent" {% if ordering == "recent" %}selected{% endif %}>Recent</option>
# <option value="support" {% if ordering == "support" %}selected{% endif %}>Most Supported</option>
# </select>

class AddIdeaForm(forms.Form):
    name = forms.CharField(max_length=50,
                            error_messages={'required':'A name is required.'},
                            widget=forms.TextInput(attrs={'placeholder': 'title'}),)

    description = forms.CharField(widget=forms.Textarea(),
                                  error_messages={'required':'A description is required.'})

    what_kind = forms.ModelChoiceField(queryset=IdeaType.objects.all(),
                                       empty_label='',
                                       error_messages={'required':'Tell us what kind of idea this is.'})

    content_object = forms.ModelChoiceField(queryset=Location.objects.all().order_by('name'),
                                   empty_label='',
                                    error_messages={'required':'You must tell where it is.'}, required=False)

    content_object_place = forms.ModelChoiceField(queryset=Place.objects.all(),
                                            empty_label='',
                                            error_messages={'required':'You must tell where it is.'}, required=False)

    what_for = forms.ChoiceField(choices=FOR_CHOICES_AND_EMPTY,
                                 error_messages={'required':'Please specify what this is for.'},
                                 widget=forms.Select())

    links = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'link examples'}),required=False)

    pic1 = forms.ImageField(widget=FilePicker, required=False)
    pic2 = forms.ImageField(widget=FilePicker, required=False)
    pic3 = forms.ImageField(widget=FilePicker, required=False)
    pic4 = forms.ImageField(widget=FilePicker, required=False)

    def clean(self, *args, **kwargs):
        cleaned_data = super(AddIdeaForm, self).clean(*args, **kwargs)
        cleaned_data = dict(cleaned_data.items() + self.files.items())
        return cleaned_data

    def is_valid(self, *args, **kwargs):
        t = super(AddIdeaForm, self).is_valid(*args, **kwargs)
        return t



    # def clean(self, *args, **kwargs):
    #     cleaned_data = super(AddIdeaNeighborhoodForm, self).clean(*args, **kwargs)
    #     cleaned_data = dict(cleaned_data.items() + self.files.items())
    #     return cleaned_data



class FilterForm(forms.Form):
    order = forms.ChoiceField(choices=REFINE_CHOICES, required=False)
    # org = forms.IntegerField(widget=forms.HiddenInput(), initial=0, required=False)
    where_place = forms.ModelChoiceField(queryset=Place.objects.none(), empty_label='where', required=False)
    where_location = forms.ModelChoiceField(queryset=Location.objects.none(), empty_label='where', required=False)
    when = forms.ChoiceField(choices=FOR_CHOICES_AND_EMPTY, required=False)
    what = forms.ModelChoiceField(queryset=IdeaType.objects.all(), empty_label='what', required=False)

    def is_valid(self):
        super(FilterForm, self).is_valid()
        return True