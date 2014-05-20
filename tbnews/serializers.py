from django.forms import widgets
from rest_framework import serializers
from models import NewsItem


class NewsItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = NewsItem
        fields = ('id', 'subject', 'content', 'img')
