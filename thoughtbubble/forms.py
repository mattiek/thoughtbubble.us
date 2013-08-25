# -*- coding: utf-8 -*-
from django import forms
from django.forms import ModelForm
from models import *

class SignupForm(ModelForm):
    confirm = forms.CharField(max_length=50, widget=forms.PasswordInput(attrs={'placeholder': 'Confirm'}))
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
            'username': forms.TextInput(attrs={'placeholder': 'Username'}),
            'location': forms.TextInput(attrs={'placeholder': 'Location'}),
            'email': forms.EmailInput(attrs={'placeholder': 'Email'}),
            'password': forms.PasswordInput(attrs={'placeholder': 'Password'}),
            }

    def __init__(self, captcha_choices, *args, **kwargs):
        super(SignupForm, self).__init__(*args, **kwargs)
        captcha_choices = captcha_choices
        if captcha_choices:
            self.fields['captcha'].choices = captcha_choices

