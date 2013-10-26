from django.shortcuts import render, redirect, HttpResponse

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

from vanilla.views import FormView as VanillaFormView

from braces.views import AjaxResponseMixin, JSONResponseMixin

from forms import UserProfileForm

from django.contrib.flatpages.models import FlatPage


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

def home(request, state=None, city=None):
    if not state or not city:
        return redirect( reverse('home',  args=[request.session.get('exploring_state','oh'),
                                                request.session.get('exploring_city','columbus'),
                                            ]))
    try:
        copy = FlatPage.objects.get(url='home').content
    except:
        copy = 'Copy here'
    d = {'copy': copy}
    return render(request, 'home.html', d)


def logout(request):
    django_logout(request)
    return redirect('home')


def explore(request, state=None, city=None, pk=None):

    if state:
        request.session['exploring_state'] = state

    if city:
        request.session['exploring_city'] = city

    d = {}
    d['communities'] = Community.objects.filter().order_by('neighborhood__name')

    d['metros'] = {
        'current': city if city else 'Columbus',
        'list': Neighborhood.objects.values_list('city','state').distinct(),
    }

    if pk:
        d['exploring'] = Community.objects.get(pk=pk)

    return render(request, 'explore.html', d)


def sherlock(request, state=None, city=None, pk=None):

    if state:
        request.session['exploring_state'] = state

    if city:
        request.session['exploring_city'] = city

    d = {}
    d['communities'] = Community.objects.filter().order_by('neighborhood__name')

    d['exploring'] = Community.objects.get(pk=pk)

    return render(request, 'sherlock.html', d)


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
                return HttpResponse('{"success":true}',content_type='application/json')


    return HttpResponse('{"success":false}',content_type='application/json')


# def dashboard(request):
#         if not request.user.is_authenticated():
#             return redirect('home')
#         try:
#             profile = ThoughtbubbleUserProfile.objects.get(user=request.user)
#         except:
#             profile = ThoughtbubbleUserProfile.objects.create(user=request.user).save()
#         d = {}
#         d['profile'] = profile
#
#         filter = request.GET.get('filter',None)
#
#         if filter == 'support':
#             d['ideas'] = [x.idea for x in IdeaSupport.objects.filter(user=request.user).order_by('-date_created')]
#         else:
#             d['ideas'] = Idea.objects.filter(user=request.user).order_by('-date_created')
#
#         return render(request, 'accounts/dashboard.html', d)


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
            user_profile = ThoughtbubbleUserProfile.objects.create(user=user, location=cleaned_data['location'])
            if cleaned_data['profile_picture']:
                avatar = Avatar.objects.create(user=user,primary=True, avatar=cleaned_data['profile_picture'])

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

    def post(self, request, *args, **kwargs):
        if 'first_name' in request.POST:
            profile_form = UserProfileForm(request.POST)
            if profile_form.is_valid():
                profile = ThoughtbubbleUserProfile.objects.get(user=request.user)
                cleaned_data =  profile_form.clean()
                profile.first_name = cleaned_data['first_name']
                profile.last_name = cleaned_data['last_name']
                profile.location = cleaned_data['location']
                profile.save()
                return redirect('user_dashboard')
        else:
            return super(MyConnectionsView, self).post(request, *args, **kwargs)


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

        u_form = UserProfileForm()
        if profile:
            u_form.fields['first_name'].initial = profile.first_name
            u_form.fields['last_name'].initial = profile.last_name
            u_form.fields['location'].initial = profile.location
        context['update_form'] = u_form

        return context


class UserProfileFormView(VanillaFormView,AjaxResponseMixin, JSONResponseMixin):
    form_class = UserProfileForm
    template_name = "accounts/update.html"