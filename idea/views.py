from django.shortcuts import render, HttpResponse, redirect
from forms import AddIdeaForm
from models import Idea, IdeaType, IdeaImage, IdeaLink, IdeaSupport
from neighborhood.models import Neighborhood
from location.models import Location
from django.contrib import messages
from vanilla import ListView, DetailView, CreateView, DeleteView
from django.contrib.comments.views.comments import post_comment
import json as JSON
from filters import IdeaFilter
from django.db.models import Q, Count

def addidea(request, state, city, id=None, community=None):
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
                        where=data['where'],
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
            return redirect(idea.where.get_absolute_url())

    else:
        form = AddIdeaForm()

    d = {'form': form}

    if id:
        form.fields['where'].initial = Location.objects.get(pk=id)

    if community:
        form.fields['where'].initial = Location.objects.get(community__name__iexact=community,
                                                            community__city__iexact=city,
                                                            community__state__iexact=state)


    return render(request, 'addidea.html', d)


class IdeaList(ListView):
    model = Idea


    def get_queryset(self):
        self.community = self.kwargs.get('community', None)
        self.city = self.kwargs.get('city', None)
        self.state = self.kwargs.get('state', None)
        if self.community:
            return Idea.objects.filter(where__community__city__iexact=self.city,
                                       where__community__state__iexact=self.state,
                                       where__community__name__iexact=self.community)
        if self.city and self.state:
            return Idea.objects.filter(where__community__city__iexact=self.city,
                                       where__community__state__iexact=self.state)
        if self.state:
            return Idea.objects.filter(where__community__state__iexact=self.state)
        return Idea.objects.filter()

    def get_context_data(self, **kwargs):
        context = super(IdeaList, self).get_context_data(**kwargs)
        f = IdeaFilter(self.request.GET, queryset=self.get_queryset(), city=self.city, state=self.state)

        ordering = self.request.GET.get('order',None)

        context['ideas'] = self.get_queryset()

        if (ordering == 'support'):
            context['ideas'] = f.qs.annotate(num_books=Count('ideasupport')).order_by('-num_books')
        else:
            context['ideas'] = f.qs.order_by('-date_created')

        context['idea_filter'] = f

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
    return redirect('idea_detail', idea.where.community.state,
                    idea.where.community.city, idea.where.community.name, id)


