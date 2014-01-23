from django.shortcuts import render, HttpResponse, redirect
from forms import AddIdeaForm, FilterForm
from models import Idea, IdeaType, IdeaImage, IdeaLink, IdeaSupport
from geo.location.models import Location
from django.contrib import messages
from vanilla import ListView, DetailView, CreateView, DeleteView
from django.contrib.comments.views.comments import post_comment
import json as JSON
# from filters import IdeaFilter
from django.db.models import Q, Count
from django.core.urlresolvers import reverse

from geo.organization.models import Organization
from geo.location.models import Location


# def add_neighborhood_idea(request, state, city, neighborhood):
#     if not request.user.is_authenticated():
#         messages.add_message(request, messages.ERROR, "Please log in to add an idea.")
#         return redirect('home')
#
#     if request.POST:
#         form = AddIdeaNeighborhoodForm(request.POST,request.FILES)
#         if form.is_valid():
#
#             data = form.cleaned_data
#
#             idea = Idea(
#                 name=data['name'],
#                 description=data['description'],
#                 what_kind=data['what_kind'],
#                 content_object=data['content_object'],
#                 what_for=data['what_for'],
#                 user=request.user
#             )
#             idea.save()
#
#             pic1 = IdeaImage(idea=idea,img=form.cleaned_data['pic1'])
#             pic2 = IdeaImage(idea=idea,img=form.cleaned_data['pic2'])
#             pic3 = IdeaImage(idea=idea,img=form.cleaned_data['pic3'])
#             pic4 = IdeaImage(idea=idea,img=form.cleaned_data['pic4'])
#
#             link1 = IdeaLink(idea=idea,url=form.cleaned_data['links'])
#
#             if link1:
#                 link1.save()
#
#             # TODO: More elegant
#             if pic1.img:
#                 pic1.save()
#             if pic2.img:
#                 pic2.save()
#             if pic3.img:
#                 pic3.save()
#             if pic4.img:
#                 pic4.save()
#
#             messages.add_message(request, messages.INFO, ' %s idea added.' % (idea.name,))
#             return redirect(idea.content_object.get_absolute_url())
#
#     else:
#         form = AddIdeaForm()
#
#     d = {'form': form,
#          'action': reverse('add_neighborhood_idea', args=[neighborhood]) }
#
#     form.fields['content_object'].queryset = Neighborhood.objects.filter(pk=neighborhood)
#     form.fields['content_object'].initial = Neighborhood.objects.filter(pk=neighborhood)
#
#     return render(request, 'addidea.html', d)



def addidea(request, id=None, organization=None, location=None):
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


    d = {'form': form,
         'action': reverse('addidea', args=[organization]) }

    if id:
        form.fields['content_object'].initial = Location.objects.get(pk=id)

    if organization:
        try:
            d['location'] = Location.objects.get(
                                                organization__title__iexact=organization,
                                                name=location)
            form.fields['content_object'].initial = d['location']
        except:
            pass



    return render(request, 'addidea.html', d)


class IdeaList(ListView):
    model = Idea


    def get_queryset(self):
        qs = super(IdeaList, self).get_queryset()
        ### Basic parameters
        self.organization = None
        try:
            self.organization = Organization.objects.get(title__iexact=self.kwargs.get('organization', None))
        except:
            pass

        self.city = self.kwargs.get('city', None)
        self.state = self.kwargs.get('state', None)

        ### Ordering
        ordering = self.request.GET.get('order',None)
        if (ordering == 'support'):
            qs = qs.annotate(num_books=Count('ideasupport')).order_by('-num_books')
        else:
            qs = qs.order_by('-date_created')


        ### Check to see that we are on an Organization Idea List page
        if self.organization:
            organizations = Organization.objects.filter(title__iexact=self.organization.title).values_list('pk', flat=True)

            ### Where
            where = self.request.GET.get('where',None)
            if where:
                locations = Location.objects.filter(pk=where)
            else:
                locations = Location.objects.filter(organization__in=organizations)
            qs = qs.filter(content_type__name='location', object_id__in=locations)
            return qs

        # neighborhood = self.kwargs.get('neighborhood', None)
        return Idea.objects.filter() #content_type__name='neighborhood', object_id=neighborhood)

        ### DEPERECATED
        # if self.organization:
        #     return Idea.objects.filter(content_object__organization__neighborhood__city__iexact=self.city,
        #                                content_object__organization__neighborhood__state__iexact=self.state,
        #                                content_object__organization__title__iexact=self.organization)
        # if self.city and self.state:
        #     return Idea.objects.filter(content_object__organization__neighborhood__city__iexact=self.city,
        #                                content_object__organization__neighborhood__state__iexact=self.state)
        # if self.state:
        #     return Idea.objects.filter(content_object__organization__neighborhood__state__iexact=self.state)
        # return Idea.objects.filter()


    def get_context_data(self, **kwargs):
        context = super(IdeaList, self).get_context_data(**kwargs)
        # f = IdeaFilter(self.request.GET, queryset=self.get_queryset(), city=self.city, state=self.state)

        f = FilterForm(self.request.GET)
        # f.fields['where'].initial = Location.objects.filter(organization=self.organization)
        f.fields['where'].queryset = Location.objects.filter(organization=self.organization)
        f.fields['where'].empty_label = self.organization.title

        context['filterform'] = f


        ordering = self.request.GET.get('order',None)

        context['ideas'] = self.object_list

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


def support_idea(request, id):
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


