from django.shortcuts import render, redirect

from forms import SignupForm, LoginForm
import random
from models import *
from django.contrib.auth import authenticate, logout as django_logout, login as django_login
from thoughtbubble.utils import path_and_rename
from community.models import Community
from idea.models import Idea, IdeaSupport

def home(request):
    return render(request, 'home.html')


def logout(request):
    django_logout(request)
    return redirect('home')


def explore(request, state=None, city=None, pk=None):
    d = {}
    d['communities'] = Community.objects.filter().order_by('neighborhood__name')

    d['metros'] = {
        'current': 'Columbus',
        'list': Neighborhood.objects.values_list('city','state').distinct(),
    }

    if pk:
        d['exploring'] = Community.objects.get(pk=pk)

    return render(request, 'explore.html', d)


def privacy(request):
    return render(request, 'privacy.html')

def login(request):
    if request.POST:
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            username = ''
            try:
                username = ThoughtbubbleUser.objects.get(email=email)
                if username:
                    username = username.username
            except:
                pass

            user = authenticate(username=username, password=password)
            if (user):
                django_login(request, user)


    return redirect('home')


def dashboard(request):
        try:
            profile = ThoughtbubbleUserProfile.objects.get(user=request.user)
        except:
            profile = ThoughtbubbleUserProfile.objects.create(user=request.user).save()
        d = {}
        d['profile'] = profile

        filter = request.GET.get('filter',None)

        if filter == 'support':
            d['ideas'] = [x.idea for x in IdeaSupport.objects.filter(user=request.user).order_by('-date_created')]
        else:
            d['ideas'] = Idea.objects.filter(user=request.user).order_by('-date_created')

        return render(request, 'accounts/dashboard.html', d)


def signup(request):
    register_captcha = 'register_captchas1234'
    if not request.session.get(register_captcha):
        # TODO: Create a lot more options
        x = [ ('guitarist','guitarist.png', ),
        ('hot dog trunk','hot-dog-truck.png', ),
        ('jimmy the dinosaur','jimmy-the-dinosaur.png', ), ]
        random.shuffle(x)
        answer = random.choice(x)
        request.session[register_captcha] = { 'answer': answer, 'choices': x }

    s = request.session.get(register_captcha)

    if request.POST:
        form = SignupForm(request.POST, request.FILES, captcha_choices=s['choices'], answer=s['answer']) # A form bound to the POST data
        if form.is_valid():
            cleaned_data = form.cleaned_data

            # create user here
            user = ThoughtbubbleUser.objects.create_user(cleaned_data['username'],
                                                         cleaned_data['email'],
                                                         cleaned_data['password'])
            django_logout(request)
            user = authenticate(username=cleaned_data['username'], email= cleaned_data['email'], password=cleaned_data['password'])

            # Create initial profile for the user
            user_profile = ThoughtbubbleUserProfile.objects.create(user=user, location=cleaned_data['location'], profile_picture=cleaned_data['profile_picture'])

            django_login(request, user)
            return redirect('home')
    else:
        form = SignupForm(captcha_choices=s['choices'], answer=s['answer'])

    return render(request, 'signup.html', {'form': form, 'captcha_answer': s['answer']})