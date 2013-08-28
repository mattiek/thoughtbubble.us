# -*- coding: utf-8 -*-
from django import forms
from django.forms import ModelForm
from models import *


class AddIdeaForm(forms.ModelForm):

    class Meta:
        model = Idea
        exclude = ['images','links',]
