from models import Community
from django.shortcuts import render, HttpResponse, redirect
from serializers import CommunitySerializer, CustomPaginationSerializer
from rest_framework import viewsets
from vanilla import DetailView, CreateView, UpdateView, ListView
from django.core.urlresolvers import reverse_lazy, reverse

class CommunityViewset(viewsets.ModelViewSet):
    serializer_class = CommunitySerializer
    queryset = Community.objects.none()
    paginate_by = None
    # pagination_serializer_class = CustomPaginationSerializer

    def get_queryset(self):
        name = self.request.GET.get('city','')
        return Community.objects.filter(neighborhood__city__icontains=name)


class CommunityList(ListView):
    model = Community


class CommunityCreate(CreateView):
    model = Community


class CommunityDetail(DetailView):
    model = Community

class CommunityUpdate(UpdateView):
    model = Community
    # success_url = reverse_lazy('community_detail')

    # def get_success_url(self, *args, **kwargs):
    #     # super(UpdateView, self).get_success_url(*args, **kwargs)
    #     return reverse('community_detail', kwargs=self.kwargs)

    def form_valid(self, form):
        s = super(CommunityUpdate,self).form_valid(form)
        return s


def join(request, state, city, pk):

    if not request.user.is_authenticated():
        return HttpResponse('none')

    try:
        comm = Community.objects.get(pk=pk)
    except:
        return HttpResponse('no community')

    g = Community.objects.filter(pk=pk,members=request.user)
    if not g:
        comm.members.add(request.user)
        return HttpResponse("added")
    else:
        comm.members.remove(request.user)
        return HttpResponse("removed")


def join_from_community(request, state, city, pk):
    join(request,state,city,pk)
    return redirect('community_detail', state, city, pk)