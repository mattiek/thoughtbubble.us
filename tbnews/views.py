from django.shortcuts import render
from django.core.urlresolvers import reverse_lazy
from django.contrib.contenttypes.models import ContentType


from models import NewsItem
from forms import NewsItemForm

from vanilla import DetailView, UpdateView, ListView, CreateView, DeleteView

from geo.location.models import Location


class NewsItemCreateView(CreateView):
    model = NewsItem
    kind = "location"
    obj_id = 0
    form_class = NewsItemForm


    def get_context_data(self, **kwargs):
        d = super(NewsItemCreateView, self).get_context_data()
        d = dict(d, **kwargs)  # idiom to union two dicts. precedence to kwargs
        return d

    def post(self, request, *args, **kwargs):
        j = request.POST

        # assuming location
        location_type = ContentType.objects.get_for_model(Location)
        j['content_type'] = location_type.id
        self.obj_id = j['object_id'] = kwargs['obj_id']
        self.kind = kwargs['kind']

        d = super(NewsItemCreateView, self).post(request,*args, **kwargs)
        return d

    def form_valid(self, form):
        # do things here
        # form.fields['']
        d = super(NewsItemCreateView, self).form_valid(form)
        return d

    def get_success_url(self):
        success_url = reverse_lazy('list_news_items', kwargs={"obj_id": self.obj_id, "kind": self.kind })
        return success_url



class NewsItemUpdateView(UpdateView):
    model = NewsItem
    success_url = reverse_lazy('list_news_items')
    kind = "location"


class NewsItemListView(ListView):
    model = NewsItem
    kind = "location"

    def get_context_data(self, **kwargs):
        d = super(NewsItemListView, self).get_context_data()
        d = dict(d, **self.kwargs)  # idiom to union two dicts. precedence to kwargs
        return d


class NewsItemDetailView(DetailView):
    model = NewsItem
    kind = "location"

class NewsItemDeleteView(DeleteView):
    model = NewsItem
    kind = "location"
    success_url = reverse_lazy('list_news_items')



# Create your views here.
