# -*- coding: utf-8 -*-
from django import forms
from django.forms import ModelForm
from models import *
from thoughtbubble.widgets import FilePicker


class AddIdeaForm(forms.ModelForm):
    pic1 = forms.ImageField(widget=FilePicker, required=False)
    pic2 = forms.ImageField(widget=FilePicker, required=False)
    pic3 = forms.ImageField(widget=FilePicker, required=False)
    pic4 = forms.ImageField(widget=FilePicker, required=False)

    class Meta:
        model = Idea
        exclude = ['images','links',]
