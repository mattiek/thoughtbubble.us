from django.shortcuts import render, HttpResponse, redirect
from forms import AddIdeaForm
from models import Idea, IdeaType, IdeaImage, IdeaLink, IdeaSupport
from neighborhood.models import Neighborhood
from location.models import Location
from django.contrib import messages
from vanilla import ListView, DetailView, CreateView, DeleteView
from django.contrib.comments.views.comments import post_comment

def addidea(request, id=None):
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
            pics = []

            # TODO: More elegant
            if pic1.img:
                pic1.save()
            if pic2.img:
                pic2.save()
            if pic3.img:
                pic3.save()
            if pic4.img:
                pic4.save()
            #
            # # TODO: bulk_create
            # if pic1.img:
            #     idea.images.add(pic1)
            # if pic2.img:
            #     idea.images.add(pic2)
            # if pic3.img:
            #     idea.images.add(pic3)
            # if pic4.img:
            #     idea.images.add(pic4)
            #
            # idea.save()

            messages.add_message(request, messages.INFO, ' %s idea added.' % (idea.name,))
            return redirect(idea.where.get_absolute_url())

    else:
        form = AddIdeaForm()

    d = {'form': form}

    if id:
        form.fields['where'].initial = Location.objects.get(pk=id)

    return render(request, 'addidea.html', d)


class IdeaList(ListView):
    model = Idea

    def get_queryset(self):
        community = self.kwargs.get('community', None)
        city = self.kwargs.get('city', None)
        state = self.kwargs.get('state', None)
        if community:
            return Idea.objects.filter(where__community__city__iexact=city,
                                       where__community__state__iexact=state,
                                       where__community__name__iexact=community)
        if city and state:
            return Idea.objects.filter(where__community__city__iexact=city,
                                       where__community__state__iexact=state)
        if state:
            return Idea.objects.filter(where__community__state__iexact=state)
        return Idea.objects.filter()


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
    if not request.user.is_authenticated():
        return HttpResponse('none')

    try:
        idea = Idea.objects.get(pk=id)
    except:
        return HttpResponse('none')

    try:
        g = IdeaSupport.objects.get(user=request.user, idea=idea)
        g.delete()
        return HttpResponse("removed")
    except:
        IdeaSupport.objects.create(user=request.user, idea=idea)
        return HttpResponse("added")


def support_idea_from_detail(request,id):
    support_idea(request,id)
    idea = Idea.objects.get(pk=id)
    return redirect('idea_detail', idea.where.community.state,
                    idea.where.community.city, idea.where.community.name, id)


