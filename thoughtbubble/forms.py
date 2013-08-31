# -*- coding: utf-8 -*-
from django import forms
from django.forms import ModelForm
from models import *
from utils import *
from widgets import FilePicker

class SignupForm(forms.Form):


    profile_picture = forms.ImageField(widget=FilePicker)
    username = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'placeholder': 'username'}),)
    location = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'placeholder': 'location'}),)
    email = forms.CharField(max_length=254,widget=forms.EmailInput(attrs={'placeholder': 'email'}))
    password = forms.CharField(max_length=50, widget=forms.PasswordInput(attrs={'placeholder': 'password'}))
    confirm = forms.CharField(max_length=50, widget=forms.PasswordInput(attrs={'placeholder': 'retype password'}))
    captcha = forms.ChoiceField(choices=[])
    accept_tos = forms.BooleanField(widget=forms.CheckboxInput )


    answer = []


    def clean(self, *args, **kwargs):
        cleaned_data = super(SignupForm, self).clean()

        username = cleaned_data.get("username")
        location = cleaned_data.get("location")
        email = cleaned_data.get("email")
        password = cleaned_data.get("password")
        confirm = cleaned_data.get("confirm")
        accept_tos = cleaned_data.get("accept_tos")
        captcha = cleaned_data.get("captcha")

        if email_exists(email):
            raise forms.ValidationError("That email has already been used to create an account. Try another one.")

        if username_exists(username):
            raise forms.ValidationError("That username has already been used to create an account. Try another one.")

        if captcha != self.answer[0]:
            raise forms.ValidationError("You flunked the human test.")

        if password != confirm:
            raise forms.ValidationError("Your password doesn't match your confirmation.")

        if not accept_tos:
            raise forms.ValidationError("You must accept the terms and conditions before registering.")

        return cleaned_data

    def __init__(self, *args, **kwargs):
        captcha_choices = kwargs.pop('captcha_choices', None)
        self.answer = kwargs.pop('answer', [])
        super(SignupForm, self).__init__(*args, **kwargs)
        if captcha_choices:
            self.fields['captcha'].choices = captcha_choices



