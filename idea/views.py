from django.shortcuts import render, HttpResponse
from forms import AddIdeaForm
from models import Idea, IdeaType, IdeaImage, IdeaLink, IdeaSupport
from neighborhood.models import Neighborhood
from django.contrib import messages
from vanilla import ListView

def addidea(request, id=None):
    if request.POST:
        form = AddIdeaForm(request.POST,request.FILES)
        if form.is_valid():
            pic1 = IdeaImage(img=form.cleaned_data['pic1'])
            pic2 = IdeaImage(img=form.cleaned_data['pic2'])
            pic3 = IdeaImage(img=form.cleaned_data['pic3'])
            pic4 = IdeaImage(img=form.cleaned_data['pic4'])
            pics = []

            # TODO: More elegant
            if pic1.img:
                pic1.save()
                pics.append(pic1)
            if pic2.img:
                pic2.save()
                pics.append(pic2)
            if pic3.img:
                pic3.save()
                pics.append(pic3)
            if pic4.img:
                pic4.save()
                pics.append(pic4)
            data = form.cleaned_data

            idea = Idea(
                        name=data['name'],
                        description=data['description'],
                        what_kind=data['what_kind'],
                        where=data['where'],
                        what_for=data['what_for'],
                        )
            idea.save()

            # TODO: bulk_create
            if pic1.img:
                idea.images.add(pic1)
            if pic2.img:
                idea.images.add(pic2)
            if pic3.img:
                idea.images.add(pic3)
            if pic4.img:
                idea.images.add(pic4)

            idea.save()

            messages.add_message(request, messages.INFO, 'Idea Saved.')

    else:
        form = AddIdeaForm()

    d = {'form': form}

    if id:
        form.fields['where'].initial = Neighborhood.objects.get(pk=id)

    return render(request, 'addidea.html', d)


class IdeaList(ListView):
    model = Idea


def support_idea(request, id):
    try:
        g = IdeaSupport.objects.get(user=request.user, idea=id)
        g.delete()
        return HttpResponse("removed")
    except:
        IdeaSupport.objects.create(user=request.user, idea=id)
        return HttpResponse("added")
