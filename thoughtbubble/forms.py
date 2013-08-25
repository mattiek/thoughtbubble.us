# -*- coding: utf-8 -*-
from django import forms
from django.forms import ModelForm
from models import *

class SignupForm(ModelForm):
    confirm = forms.CharField(max_length=50, widget=forms.PasswordInput(attrs={'placeholder': 'retype password'}))
    captcha = forms.ChoiceField(choices=[])
    accept_tos = forms.BooleanField(widget=forms.CheckboxInput )

    class Meta:
        model = ThoughtbubbleUser
        fields = [
                  'username',
                  'location',
                  'email',
                  'password',
        ]
        widgets = {
            'username': forms.TextInput(attrs={'placeholder': 'username'}),
            'location': forms.TextInput(attrs={'placeholder': 'location'}),
            'email': forms.EmailInput(attrs={'placeholder': 'email'}),
            'password': forms.PasswordInput(attrs={'placeholder': 'password'}),
            }

    def __init__(self, captcha_choices, *args, **kwargs):
        super(SignupForm, self).__init__(*args, **kwargs)
        captcha_choices = captcha_choices
        if captcha_choices:
            self.fields['captcha'].choices = captcha_choices

