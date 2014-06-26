from django.shortcuts import render
from django.core.urlresolvers import reverse_lazy
from django.contrib.contenttypes.models import ContentType


from models import NewsItem
from .serializers import NewsItemSerializer
from forms import NewsItemForm

from vanilla import DetailView, UpdateView, ListView, CreateView, DeleteView

from geo.location.models import Location
from geo.organization.models import Organization
from rest_framework import viewsets



class NewsItemCreateView(CreateView):
    model = NewsItem
    kind = "location"
    obj_id = 0
    form_class = NewsItemForm


    def get_context_data(self, **kwargs):
        d = super(NewsItemCreateView, self).get_context_data()
        d = dict(d, **kwargs)  # idiom to union two dicts. precedence to kwargs

        c_type = 'location'
        if self.kwargs.get('kind') == 'org':
            c_type = 'organization'

        d['form'].fields['content_type'].initial = d['form'].fields['content_type'].choices.queryset.get(name=c_type).id
        d['form'].fields['object_id'].initial = self.kwargs.get('obj_id')
        return d

    def post(self, request, *args, **kwargs):
        j = request.POST

        location_type = ContentType.objects.get(pk=j['content_type'])
        self.obj_id = j['object_id']
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

    def get_success_url(self):
        return reverse_lazy('list_news_items', args=[self.kwargs.get('kind'), self.kwargs.get('obj_id')])


class NewsItemListView(ListView):
    model = NewsItem
    kind = "location"
    c_type = 'location'

    def get_queryset(self):
        qs = super(NewsItemListView, self).get_queryset()
        if self.kwargs.get('kind') == 'org':
            self.c_type = 'organization'
        c = ContentType.objects.get(name=self.c_type)
        return qs.filter(content_type=c, object_id=self.kwargs.get('obj_id'))

    def get_context_data(self, **kwargs):
        d = super(NewsItemListView, self).get_context_data()
        d = dict(d, **self.kwargs)  # idiom to union two dicts. precedence to kwargs
        obj_id = self.kwargs.get('obj_id')
        if self.c_type == 'organization':
            o = Organization.objects.get(pk=obj_id)
        else:
            o = Location.objects.get(pk=obj_id)
        d['obj'] = o
        return d


class NewsItemDetailView(DetailView):
    model = NewsItem
    kind = "location"

class NewsItemDeleteView(DeleteView):
    model = NewsItem

    def get_success_url(self):
        return reverse_lazy('list_news_items', args=[self.kwargs.get('kind'), self.kwargs.get('obj_id')])



class NewsItemViewset(viewsets.ModelViewSet):
    model = NewsItem
    serializer_class = NewsItemSerializer
    queryset = NewsItem.objects.all()

    def get_queryset(self):
        qs = super(NewsItemViewset, self).get_queryset()
        kind = self.request.GET.get('kind',None)
        c = ContentType.objects.get(name=kind)
        return qs.filter(content_type=c, object_id=self.request.GET.get('obj_id'))
