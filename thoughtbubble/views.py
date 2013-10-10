from django.shortcuts import render, redirect

from forms import SignupForm, LoginForm
import random
from models import *
from django.contrib.auth import authenticate, logout as django_logout, login as django_login
from thoughtbubble.utils import path_and_rename
from community.models import Community
from idea.models import Idea, IdeaSupport

from django.views.generic.edit import FormView
from django.core.urlresolvers import reverse, reverse_lazy

from allauth.socialaccount.forms import DisconnectForm

from django.contrib import messages

from allauth.account.adapter import get_adapter as get_account_adapter
from allauth.socialaccount.adapter import DefaultSocialAccountAdapter

class MyDisconnectForm(DisconnectForm):
    cleaned_data = {}


class MySocialAdapter(DefaultSocialAccountAdapter):
    def get_connect_redirect_url(self, request, socialaccount):
        """
        Returns the default URL to redirect to after successfully
        connecting a social account.
        """
        assert request.user.is_authenticated()
        url = reverse('user_dashboard')
        return url

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
        if not request.user.is_authenticated():
            return redirect('home')
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


class MyConnectionsView(FormView):
    template_name = "accounts/dashboard.html"
    form_class = DisconnectForm
    success_url = reverse_lazy("user_dashboard")

    def get_form_kwargs(self):
        kwargs = super(MyConnectionsView, self).get_form_kwargs()
        kwargs["request"] = self.request
        return kwargs

    def form_valid(self, form):
        get_account_adapter().add_message(self.request,
                                          messages.INFO,
                                          'socialaccount/messages/'
                                          'account_disconnected.txt')
        form.save()
        return super(MyConnectionsView, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(MyConnectionsView,self).get_context_data(**kwargs)
        try:
            profile = ThoughtbubbleUserProfile.objects.get(user=self.request.user)
        except:
            profile = ThoughtbubbleUserProfile.objects.create(user=self.request.user).save()
        context['profile'] = profile

        filter = self.request.GET.get('filter',None)

        if filter == 'support':
            context['ideas'] = [x.idea for x in IdeaSupport.objects.filter(user=self.request.user).order_by('-date_created')]
        else:
            context['ideas'] = Idea.objects.filter(user=self.request.user).order_by('-date_created')

        return context
