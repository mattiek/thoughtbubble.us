from django.shortcuts import render
from forms import AddIdeaForm
from models import Idea, IdeaType, IdeaImage, IdeaLink


def addidea(request):
    if request.POST:
        form = AddIdeaForm(request.POST,request.FILES)
        if form.is_valid():
            pic1 = IdeaImage(img=form.cleaned_data['pic1'])
            pic2 = IdeaImage(img=form.cleaned_data['pic2'])
            pic3 = IdeaImage(img=form.cleaned_data['pic3'])
            pic4 = IdeaImage(img=form.cleaned_data['pic4'])
            pic1.save()

    else:
        form = AddIdeaForm()

    return render(request, 'addidea.html', {'form': form})


def listideas(request):
    pass
