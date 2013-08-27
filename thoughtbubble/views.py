from django.shortcuts import render, redirect

from forms import SignupForm
import random
from models import *
from django.contrib.auth import authenticate, logout as django_logout, login

def home(request):

    return render(request, 'home.html')

def logout(request):
    django_logout(request)
    return redirect('home')

def signup(request):
    register_captcha = 'register_captchas1234'
    if not request.session.get(register_captcha):
        x = [ ('guitarist','guitarist.png', ),
        ('hot dog trunk','hot-dog-truck.png', ),
        ('jimmy the dinosaur','jimmy-the-dinosaur.png', ), ]
        random.shuffle(x)
        answer = random.choice(x)
        request.session[register_captcha] = { 'answer': answer, 'choices': x }

    s = request.session.get(register_captcha)

    if request.POST:
        form = SignupForm(request.POST, captcha_choices=s['choices'], answer=s['answer']) # A form bound to the POST data
        if form.is_valid():
            cleaned_data = form.cleaned_data

            # create user here
            user = ThoughtbubbleUser.objects.create_user(cleaned_data['username'],
                                                         cleaned_data['email'],
                                                         cleaned_data['location'],
                                                         cleaned_data['password'])
            user.save()
            django_logout(request)
            user = authenticate(username=cleaned_data['username'], email= cleaned_data['email'], password=cleaned_data['password'])
            login(request, user)
            return redirect('home')
    else:
        form = SignupForm(captcha_choices=s['choices'], answer=s['answer'])

    return render(request, 'signup.html', {'form': form, 'captcha_answer': s['answer']})