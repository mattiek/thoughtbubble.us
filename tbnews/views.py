from django.shortcuts import render
from models import NewsItem

from vanilla import DetailView, UpdateView, ListView, CreateView


class NewsItemCreateView(CreateView):
    model = NewsItem


class NewsItemUpdateView(UpdateView):
    model = NewsItem

class NewsItemListView(ListView):
    model = NewsItem

class NewsItemDetailView(DetailView):
    model = NewsItem



# Create your views here.
