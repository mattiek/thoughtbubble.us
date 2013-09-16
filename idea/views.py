from django.shortcuts import render
from forms import AddIdeaForm
from models import Idea, IdeaType, IdeaImage, IdeaLink
from neighborhood.models import Neighborhood
from django.contrib import messages


def addidea(request, id=None):
    if request.POST:
        form = AddIdeaForm(request.POST,request.FILES)
        if form.is_valid():
            pic1 = IdeaImage(img=form.cleaned_data['pic1'])
            pic2 = IdeaImage(img=form.cleaned_data['pic2'])
            pic3 = IdeaImage(img=form.cleaned_data['pic3'])
            pic4 = IdeaImage(img=form.cleaned_data['pic4'])
            pic1.save()
            pic2.save()
            pic3.save()
            pic4.save()
            idea = Idea(pic1=pic1, pic2=pic2, pic3=pic3, pic4=pic4)
            idea.save()
            messages.add_message(request, messages.INFO, 'Idea Saved.')

    else:
        form = AddIdeaForm()

    d = {'form': form}

    if id:
        form.fields['where'].initial = Neighborhood.objects.get(pk=id)

    return render(request, 'addidea.html', d)


def listideas(request):
    pass
