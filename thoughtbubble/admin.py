from django import forms
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.contrib.flatpages.models import FlatPage

from .models import *

class ThoughtbubbleUserCreationForm(forms.ModelForm):
    password1 = forms.CharField(
        label='Password',
        widget=forms.PasswordInput)
    password2 = forms.CharField(
        label='Password confirmation',
        widget=forms.PasswordInput)

    class Meta:
        model = ThoughtbubbleUser
        fields = ('username',)

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            msg = "Passwords don't match"
            raise forms.ValidationError(msg)
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super(ThoughtbubbleUserCreationForm,
                     self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class ThoughtbubbleUserChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField(label= ("Password"),
                                         help_text= ("Raw passwords are not stored, so there is no way to see "
                                                     "this user's password, but you can change the password "
                                                     "using <a href=\"password/\">this form</a>."))

    class Meta:
        model = ThoughtbubbleUser

    def clean_password(self):
        # Regardless of what the user provides, return the
        # initial value. This is done here, rather than on
        # the field, because the field does not have access
        # to the initial value
        return self.initial["password"]


class ThoughtbubbleUserAdmin(UserAdmin):
    add_form = ThoughtbubbleUserCreationForm
    form = ThoughtbubbleUserChangeForm

    list_display = ('username', 'is_staff',)
    list_filter = ('is_staff', 'is_superuser',
                   'is_active', 'groups',)
    search_fields = ('username',)
    ordering = ('username',)
    filter_horizontal = ('groups', 'user_permissions',)
    fieldsets = (
        (None, {'fields': ('username', 'email', 'password',)}),
        # ('Personal info', {'fields':
        #                        ('location',)}),
        ('Permissions', {'fields': ('is_active',
                                    'is_staff',
                                    'is_superuser',
                                    'groups',
                                    'user_permissions')}),
        ('Important dates', {'fields': ('last_login',)}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username',
                       'password1', 'password2')}
        ),
    )


from django import forms
from django.contrib.flatpages.admin import FlatpageForm, FlatPageAdmin
from tinymce.widgets import TinyMCE


class PageForm(FlatpageForm):

    class Meta:
        model = FlatPage
        widgets = {
            'content' : TinyMCE(attrs={'cols': 100, 'rows': 65}),
            }


class PageAdmin(FlatPageAdmin):
    """
    Page Admin
    """
    form = PageForm

class FlatPageForm(forms.ModelForm):
    content = forms.CharField(widget=TinyMCE(
                        attrs={'cols': 80, 'rows': 90},
                        mce_attrs={
                            'plugins': "fullscreen,table,spellchecker,paste,searchreplace",
                            'theme': "advanced",
                            'theme_advanced_buttons1_add' : "fullscreen",
                        },
    ))

    class Meta:
        model = FlatPage

from tinymce.widgets import TinyMCE
class FlatPageAdmin(admin.ModelAdmin):
    form = FlatPageForm

    class Media:
        css = {'all': ["css/tb-privacy.css",]}
    #     js = ("//tinymce.cachefly.net/4.0/tinymce.min.js","js/tb/flatpage.js",)
    #     pass

admin.site.register(ThoughtbubbleUser, ThoughtbubbleUserAdmin)
admin.site.register(ThoughtbubbleUserProfile)

# admin.site.unregister(FlatPage)
# admin.site.register(FlatPage, FlatPageAdmin)

admin.site.unregister(FlatPage)
# admin.site.register(FlatPage, PageAdmin)

from django import forms
from django.core.urlresolvers import reverse
from django.contrib.flatpages.admin import FlatPageAdmin
from django.contrib.flatpages.models import FlatPage
from tinymce.widgets import TinyMCE

class TinyMCEFlatPageAdmin(FlatPageAdmin):
    def formfield_for_dbfield(self, db_field, **kwargs):
        if db_field.name == 'content':
            return db_field.formfield(widget=TinyMCE(
                attrs={'cols': 80, 'rows': 30},
                mce_attrs={
                    'external_link_list_url': reverse('tinymce.views.flatpages_link_list'),
                    # 'plugin_preview_pageurl': reverse('tinymce-preview', "thoughtbubble"),
                    'plugins': "fullscreen,table,spellchecker,paste,searchreplace",
                    'theme': "advanced",
                    'theme_advanced_buttons1_add' : "fullscreen",
                },
                ))
        return super(TinyMCEFlatPageAdmin, self).formfield_for_dbfield(db_field, **kwargs)

admin.site.register(FlatPage, TinyMCEFlatPageAdmin)