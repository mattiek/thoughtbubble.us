# -*- coding: utf-8 -*-
from django import forms
from django.forms import ModelForm
from models import *
from thoughtbubble.widgets import FilePicker


FOR_CHOICES_AND_EMPTY = [('','')] + FOR_CHOICES

class AddIdeaForm(forms.Form):
    name = forms.CharField(max_length=50,
                            error_messages={'required':'A name is required.'},
                            widget=forms.TextInput(attrs={'placeholder': 'title'}),)

    description = forms.CharField(widget=forms.Textarea(),
                                  error_messages={'required':'A description is required.'})

    what_kind = forms.ModelChoiceField(queryset=IdeaType.objects.all(),
                                       empty_label='',
                                       error_messages={'required':'Tell us what kind of idea this is.'})

    where = forms.ModelChoiceField(queryset=Location.objects.filter(organization__neighborhood__city='Columbus').order_by('name'),
                                   empty_label='',
                                    error_messages={'required':'You must tell where it is.'})

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

