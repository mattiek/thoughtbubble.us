from django.contrib import admin
from django import forms
from tinymce.widgets import TinyMCE
from models import NewsItem


class NewsItemForm(forms.ModelForm):
    content = forms.CharField(widget=TinyMCE(
        attrs={'cols': 80, 'rows': 90},
        mce_attrs={
            'plugins': "fullscreen,table,spellchecker,paste,searchreplace",
            'theme': "advanced",
            'theme_advanced_buttons1_add' : "fullscreen",
            },
        ))

    class Meta:
        model = NewsItem


class NewsItemAdmin(admin.ModelAdmin):
    form = NewsItemForm


admin.site.register(NewsItem, NewsItemAdmin)
# Register your models here.
