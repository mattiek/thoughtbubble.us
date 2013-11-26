from django.forms import forms, ModelForm
from django.forms.widgets import HiddenInput

from models import NewsItem


class NewsItemForm(ModelForm):

    class Meta:
        model = NewsItem
        widgets = {
            'object_id':  HiddenInput(),
            'content_type': HiddenInput(),
        }

        #fields = ['subject', 'content', 'img']


    def clean(self):
        d = super(NewsItemForm, self).clean()
        return d


