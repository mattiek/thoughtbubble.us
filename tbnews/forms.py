from django.forms import forms, ModelForm

from models import NewsItem


class NewsItemForm(ModelForm):

    class Meta:
        model = NewsItem
