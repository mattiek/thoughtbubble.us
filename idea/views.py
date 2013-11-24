from django.shortcuts import render, HttpResponse, redirect
from forms import AddIdeaForm
from models import Idea, IdeaType, IdeaImage, IdeaLink, IdeaSupport
from neighborhood.models import Neighborhood
from location.models import Location
from django.contrib import messages
from vanilla import ListView, DetailView, CreateView, DeleteView
from django.contrib.comments.views.comments import post_comment
import json as JSON
# from filters import IdeaFilter
from django.db.models import Q, Count

from organization.models import Organization
from location.models import Location

def addidea(request, state, city, id=None, organization=None, location=None):
    if not request.user.is_authenticated():
        messages.add_message(request, messages.ERROR, "Please log in to add an idea.")
        return redirect('home')

    if request.POST:
        form = AddIdeaForm(request.POST,request.FILES)
        if form.is_valid():

            data = form.cleaned_data

            idea = Idea(
                        name=data['name'],
                        description=data['description'],
                        what_kind=data['what_kind'],
                        content_object=data['content_object'],
                        what_for=data['what_for'],
                        user=request.user
                        )
            idea.save()

            pic1 = IdeaImage(idea=idea,img=form.cleaned_data['pic1'])
            pic2 = IdeaImage(idea=idea,img=form.cleaned_data['pic2'])
            pic3 = IdeaImage(idea=idea,img=form.cleaned_data['pic3'])
            pic4 = IdeaImage(idea=idea,img=form.cleaned_data['pic4'])

            link1 = IdeaLink(idea=idea,url=form.cleaned_data['links'])

            if link1:
                link1.save()

            # TODO: More elegant
            if pic1.img:
                pic1.save()
            if pic2.img:
                pic2.save()
            if pic3.img:
                pic3.save()
            if pic4.img:
                pic4.save()

            messages.add_message(request, messages.INFO, ' %s idea added.' % (idea.name,))
            return redirect(idea.content_object.get_absolute_url())

    else:
        form = AddIdeaForm()

    d = {'form': form}

    if id:
        form.fields['content_object'].initial = Location.objects.get(pk=id)

    if organization:
        d['location'] = Location.objects.get(
                                            organization__title__iexact=organization,
                                            organization__neighborhood__city__iexact=city,
                                            organization__neighborhood__state__iexact=state,
                                            name=location)
        form.fields['content_object'].initial = d['location']



    return render(request, 'addidea.html', d)


class IdeaList(ListView):
    model = Idea


    def get_queryset(self):
        ### Basic parameters
        self.organization = self.kwargs.get('organization', None)
        self.city = self.kwargs.get('city', None)
        self.state = self.kwargs.get('state', None)

        ### Ordering
        ordering = self.request.GET.get('order',None)
        if (ordering == 'support'):
            self.queryset = self.queryset.annotate(num_books=Count('ideasupport')).order_by('-num_books')
        else:
            self.queryset = self.queryset.order_by('-date_created')

        ### Check to see that we are on an Organization Idea List page
        if self.organization:
            organizations = Organization.objects.filter(title__iexact=self.organization).values_list('pk', flat=True)
            locations = Location.objects.filter(organization__in=organizations)
            return Idea.objects.filter(content_type__name='location', object_id__in=locations)

        neighborhood = self.kwargs.get('neighborhood', None)
        return Idea.objects.filter(content_type__name='neighborhood', object_id=neighborhood)


        if self.organization:
            return Idea.objects.filter(content_object__organization__neighborhood__city__iexact=self.city,
                                       content_object__organization__neighborhood__state__iexact=self.state,
                                       content_object__organization__title__iexact=self.organization)
        if self.city and self.state:
            return Idea.objects.filter(content_object__organization__neighborhood__city__iexact=self.city,
                                       content_object__organization__neighborhood__state__iexact=self.state)
        if self.state:
            return Idea.objects.filter(content_object__organization__neighborhood__state__iexact=self.state)
        return Idea.objects.filter()

    def get_context_data(self, **kwargs):
        context = super(IdeaList, self).get_context_data(**kwargs)
        # f = IdeaFilter(self.request.GET, queryset=self.get_queryset(), city=self.city, state=self.state)


        ordering = self.request.GET.get('order',None)

        context['ideas'] = self.get_queryset()

        context['ordering'] = ordering

        return context


class IdeaDetail(DetailView):
    model = Idea

    def get_context_data(self, **kwargs):
        context = super(IdeaDetail,self).get_context_data(**kwargs)
        idea = self.model.objects.get(pk=self.kwargs['pk'])
        if self.request.user.is_authenticated():
            context['supported'] = IdeaSupport.objects.filter(idea=idea,user=self.request.user)
        context['pictures'] = idea.ideaimage_set.all()
        return context


class IdeaCreate(CreateView):
    model = Idea
    form_class = AddIdeaForm


def support_idea(request, state, city, id):
    result = {'status':'none'}
    noStatus = {'status':'none'}
    removedStatus = {'status':'removed'}
    addedStatus = {'status':'added'}

    if request.user.is_authenticated():
        try:
            idea = Idea.objects.get(pk=id)
            try:
                g = IdeaSupport.objects.get(user=request.user, idea=idea)
                g.delete()
                result['status'] = 'removed'
            except:
                IdeaSupport.objects.create(user=request.user, idea=idea)
                result['status'] = 'added'
            result['count'] = idea.support_count()
        except:
            pass

    return HttpResponse(JSON.dumps(result), mimetype='application/json')

def support_idea_from_detail(request,id):
    support_idea(request,id)
    idea = Idea.objects.get(pk=id)
    return redirect('idea_detail', idea.content_object.organization.state,
                    idea.content_object.organization.city, idea.content_object.organization.name, id)


