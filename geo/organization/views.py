from models import Organization
from django.shortcuts import render, HttpResponse, redirect
from serializers import OrganizationSerializer, CustomPaginationSerializer
from rest_framework import viewsets
from vanilla import DetailView, CreateView, UpdateView, ListView
from django.core.urlresolvers import reverse_lazy, reverse
from forms import OrganizationUpdateForm

class OrganizationViewset(viewsets.ModelViewSet):
    serializer_class = OrganizationSerializer
    queryset = Organization.objects.none()
    paginate_by = None
    # pagination_serializer_class = CustomPaginationSerializer

    def get_queryset(self):
        place_id = self.request.GET.get('place','')
        org_id = self.request.GET.get('org','')
        if org_id:
            return Organization.objects.filter(pk=org_id)
        return Organization.objects.filter(place=place_id)


class OrganizationList(ListView):
    model = Organization

    def get_template_names(self):
        return self.request.device_template_dir + super(OrganizationList, self).get_template_names().pop()


class OrganizationCreate(CreateView):
    model = Organization

    def get_template_names(self):
        return self.request.device_template_dir + super(OrganizationCreate, self).get_template_names().pop()


class OrganizationDetail(DetailView):
    model = Organization
    lookup_field = 'slug'
    lookup_url_kwarg = 'organization'

    def get_template_names(self):
        return self.request.device_template_dir + super(OrganizationDetail, self).get_template_names().pop()

class OrganizationUpdate(UpdateView):
    model = Organization
    form_class = OrganizationUpdateForm
    lookup_field = 'slug'
    lookup_url_kwarg = 'organization'
    # success_url = reverse_lazy('organization_detail')

    def get_template_names(self):
        return self.request.device_template_dir + super(OrganizationUpdate, self).get_template_names().pop()

    # def get_success_url(self, *args, **kwargs):
    #     # super(UpdateView, self).get_success_url(*args, **kwargs)
    #     return reverse('organization_detail', kwargs=self.kwargs)

    def form_valid(self, form):
        s = super(OrganizationUpdate,self).form_valid(form)
        pics = [form.cleaned_data.get('pic-picture_%d' % x, None) for x in range(1,5)]
        partners = [form.cleaned_data.get('partner-picture_%d' % x, None) for x in range(1,5)]

        for x in range(0,4):
            obj = self.object.organizationimage_set.filter(ordering=x, active=True)
            # if obj:
            #     obj.active = False
            #     obj.save()
            order = x + 1
            if pics[x]:
                self.object.organizationimage_set.create(name='', img=pics[x], ordering=order,active=True)

        return s

    def form_invalid(self, form):
        s = super(OrganizationUpdate,self).form_valid(form)
        return s

    def get_context_data(self, **kwargs):
        context = super(OrganizationUpdate, self).get_context_data(**kwargs)
        return context


def join(request, place, organization):

    if not request.user.is_authenticated():
        return HttpResponse('none')

    try:
        comm = Organization.objects.get(slug=organization, place__slug=place)
    except:
        return HttpResponse('no organization')

    g = Organization.objects.filter(slug=organization, place__slug=place, members=request.user)

    if not g:
        comm.members.add(request.user)
        return HttpResponse("added")
    else:
        comm.members.remove(request.user)
        return HttpResponse("removed")


def join_from_organization(request, place, organization):
    join(request,place,organization)
    return redirect('organization_detail', place, organization)