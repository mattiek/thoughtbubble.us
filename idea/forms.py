# -*- coding: utf-8 -*-
from django import forms
from django.forms import ModelForm
from models import *
from thoughtbubble.widgets import FilePicker


FOR_CHOICES_AND_EMPTY = [('','')] + FOR_CHOICES

class AddIdeaForm(forms.Form):
    name = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'placeholder': 'title'}),)
    description = forms.CharField(widget=forms.Textarea(),)
    what_kind = forms.ModelChoiceField(queryset=IdeaType.objects.all(), empty_label='')
    where = forms.ModelChoiceField(queryset=Neighborhood.objects.filter(city='Columbus').order_by('name'), empty_label='')
    what_for = forms.ChoiceField(choices=FOR_CHOICES_AND_EMPTY,widget=forms.Select())

    pic1 = forms.ImageField(widget=FilePicker, required=False)
    pic2 = forms.ImageField(widget=FilePicker, required=False)
    pic3 = forms.ImageField(widget=FilePicker, required=False)
    pic4 = forms.ImageField(widget=FilePicker, required=False)

