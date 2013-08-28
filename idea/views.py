from django.shortcuts import render
from forms import AddIdeaForm


def addidea(request):
    form = AddIdeaForm()
    return render(request, 'addidea.html', {'form': form})