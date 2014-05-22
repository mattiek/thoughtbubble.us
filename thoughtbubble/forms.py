# -*- coding: utf-8 -*-
from django import forms
from django.forms import ModelForm
from models import *
from utils import *
from widgets import FilePicker

from model_utils import Choices

import re

def email_exists(email):
    try:
        ThoughtbubbleUser.objects.get(email=email)
        exists = True
    except:
        exists = False
    return exists

def username_exists(username):
    try:
        ThoughtbubbleUser.objects.get(username=username)
        exists = True
    except:
        exists = False
    return exists


class SignupForm(forms.Form):


    profile_picture = forms.ImageField(widget=FilePicker, required=False)
    username = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'placeholder': 'username'}),error_messages={'required':'A username is required.'})
    location = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'placeholder': 'location'}),)
    email = forms.CharField(max_length=254,widget=forms.EmailInput(attrs={'placeholder': 'email'}),error_messages={'required':'An email is required.'})
    password = forms.CharField(max_length=50, widget=forms.PasswordInput(attrs={'placeholder': 'password'}),error_messages={'required':'A password is required.'})
    confirm = forms.CharField(max_length=50, widget=forms.PasswordInput(attrs={'placeholder': 'retype password'}),error_messages={'required':'You must confirm your password.'})
    captcha = forms.ChoiceField(choices=[],error_messages={'required':'You are required to try the captcha.'})
    accept_tos = forms.BooleanField(widget=forms.CheckboxInput,error_messages={'required':'You are required to accept the terms.'} )


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

        re_match = re.match('\w+',username)
        if email_exists(email):
            raise forms.ValidationError("That email has already been used to create an account. Try another one.")

        if username_exists(username):
            raise forms.ValidationError("That username has already been used to create an account. Try another one.")

        if not re_match or re_match.group(0) != username:
            raise forms.ValidationError("Usernames can only include letters, numbers and underscores. ")

        if captcha != self.answer[0]:
            raise forms.ValidationError("You flunked the captcha.")

        if password != confirm:
            raise forms.ValidationError("Your password doesn't match your confirmation.")

        if not accept_tos:
            raise forms.ValidationError("You must accept the terms and conditions before registering.")

        cleaned_data = dict(cleaned_data.items() + self.files.items())
        return cleaned_data

    def __init__(self, *args, **kwargs):
        captcha_choices = kwargs.pop('captcha_choices', None)
        self.answer = kwargs.pop('answer', [])
        super(SignupForm, self).__init__(*args, **kwargs)
        if captcha_choices:
            self.fields['captcha'].choices = captcha_choices


class OrganizationSignupForm(SignupForm):
    organization_name = forms.CharField(max_length=250, widget=forms.TextInput(attrs={'placeholder': 'organization name'}),error_messages={'required':'You need an organization name.'})
    organization_address = forms.CharField(max_length=250, widget=forms.TextInput(attrs={'placeholder': 'organization address'}),error_messages={'required':'Organization address is required.'})
    organization_zipcode = forms.CharField(max_length=250, widget=forms.TextInput(attrs={'placeholder': 'organization zipcode'}),error_messages={'required':'Zipcode for organization is needed.'})
    organization_phone = forms.CharField(max_length=250, widget=forms.TextInput(attrs={'placeholder': 'organization phone'}),error_messages={'required':'Phone number for organization is required.'})
    organization_email = forms.CharField(max_length=250, widget=forms.TextInput(attrs={'placeholder': 'organization email'}),error_messages={'required':'We need an email for the organization.'})

    organization_contact = forms.CharField(max_length=250, widget=forms.TextInput(attrs={'placeholder': 'organization contact'}),error_messages={'required':'Who is the contact for the organization?'})
    organization_phone_number = forms.CharField(max_length=250, widget=forms.TextInput(attrs={'placeholder': 'organization contact phone number'}),error_messages={'required':'What is the phone number for the organization contact?'})
    organization_contact_email = forms.CharField(max_length=250, widget=forms.TextInput(attrs={'placeholder': 'organization contact email'}),error_messages={'required':'We need an email for the organization conrtact.'})

    organization_alt_contact = forms.CharField(max_length=250, required=False, widget=forms.TextInput(attrs={'placeholder': 'organization alt contact'}))
    organization_alt_phone_number = forms.CharField(max_length=250, required=False, widget=forms.TextInput(attrs={'placeholder': 'organization alt phone number'}))
    organization_alt_contact_email = forms.CharField(max_length=250, required=False, widget=forms.TextInput(attrs={'placeholder': 'organization alt contact email'}))

    organization_cc = forms.CharField(max_length=250,widget=forms.TextInput(attrs={'placeholder': 'credit card number'}))
    organization_cc_name = forms.CharField(max_length=250, widget=forms.TextInput(attrs={'placeholder': 'name on card'}))
    organization_expiry = forms.CharField(max_length=250, widget=forms.TextInput(attrs={'placeholder': 'expiration date'}))
    organization_security = forms.CharField(max_length=250, widget=forms.TextInput(attrs={'placeholder': 'security code'}))

    def clean(self, *args, **kwargs):
        cleaned_data = super(OrganizationSignupForm, self).clean()

        organization_name = cleaned_data.get("organization_name")
        organization_address = cleaned_data.get("organization_address")
        organization_zipcode = cleaned_data.get("organization_zipcode")
        organization_phone = cleaned_data.get("organization_phone")
        organization_email = cleaned_data.get("organization_email")

        organization_contact = cleaned_data.get("organization_contact")
        organization_phone_number = cleaned_data.get("organization_phone_number")
        organization_contact_email = cleaned_data.get("organization_contact_email")

        organization_alt_contact = cleaned_data.get("organization_alt_contact","")
        organization_alt_phone_number = cleaned_data.get("organization_alt_phone_number","")
        organization_alt_contact_email = cleaned_data.get("organization_alt_contact_email","")


        organization_cc = cleaned_data.get("organization_cc")
        organization_cc_name = cleaned_data.get("organization_cc_name")
        organization_cc_expiry = cleaned_data.get("organization_expiry")
        organization_cc_security = cleaned_data.get("organization_security")

        cleaned_data = dict(cleaned_data.items() + self.files.items())
        return cleaned_data


class UserProfileForm(forms.Form):
    first_name = forms.CharField(max_length=50,required=False)
    last_name = forms.CharField(max_length=50,required=False)
    location = forms.CharField(max_length=50,required=False)

    def clean(self, *args, **kwargs):
        cleaned_data = super(UserProfileForm, self).clean()
        return cleaned_data


class AvatarForm(forms.Form):
    pass


class LoginForm(forms.Form):
    email = forms.CharField(max_length=254,widget=forms.EmailInput(attrs={'placeholder': 'email'}))
    password = forms.CharField(max_length=50, widget=forms.PasswordInput(attrs={'placeholder': 'password'}))

    def clean(self, *args, **kwargs):
        cleaned_data = super(LoginForm, self).clean()
        return cleaned_data


class ContactForm(forms.Form):
    SUBJECTS = Choices(
                        'General',
                        'Report Misuse',

                       'Membership',
                       'Sign-Up',
                       'FAQs',
                        'Terms & Privacy')
    email = forms.EmailField()
    subject = forms.ChoiceField(choices=SUBJECTS)
    body = forms.Textarea()
