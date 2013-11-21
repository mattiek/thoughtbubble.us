from models import Organization
from django.shortcuts import render, HttpResponse, redirect
from serializers import OrganizationSerializer, CustomPaginationSerializer
from rest_framework import viewsets
from vanilla import DetailView, CreateView, UpdateView, ListView
from django.core.urlresolvers import reverse_lazy, reverse

class OrganizationViewset(viewsets.ModelViewSet):
    serializer_class = OrganizationSerializer
    queryset = Organization.objects.none()
    paginate_by = None
    # pagination_serializer_class = CustomPaginationSerializer

    def get_queryset(self):
        name = self.request.GET.get('city','')
        return Organization.objects.filter(neighborhood__city__icontains=name)


class OrganizationList(ListView):
    model = Organization


class OrganizationCreate(CreateView):
    model = Organization


class OrganizationDetail(DetailView):
    model = Organization

class OrganizationUpdate(UpdateView):
    model = Organization
    # success_url = reverse_lazy('organization_detail')

    # def get_success_url(self, *args, **kwargs):
    #     # super(UpdateView, self).get_success_url(*args, **kwargs)
    #     return reverse('organization_detail', kwargs=self.kwargs)

    def form_valid(self, form):
        s = super(OrganizationUpdate,self).form_valid(form)
        return s


def join(request, state, city, pk):

    if not request.user.is_authenticated():
        return HttpResponse('none')

    try:
        comm = Organization.objects.get(pk=pk)
    except:
        return HttpResponse('no organization')

    g = Organization.objects.filter(pk=pk,members=request.user)
    if not g:
        comm.members.add(request.user)
        return HttpResponse("added")
    else:
        comm.members.remove(request.user)
        return HttpResponse("removed")


def join_from_organization(request, state, city, pk):
    join(request,state,city,pk)
    return redirect('organization_detail', state, city, pk)