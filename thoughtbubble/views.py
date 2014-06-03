import random

from django.contrib.auth import authenticate, logout as django_logout, login as django_login
from django.views.generic.edit import FormView
from django.core.urlresolvers import reverse, reverse_lazy
from django.contrib.flatpages.models import FlatPage
from django.contrib import messages
from django.shortcuts import render, redirect, HttpResponse
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _

from allauth.socialaccount.forms import DisconnectForm
from allauth.account.adapter import get_adapter as get_account_adapter
from allauth.socialaccount.adapter import DefaultSocialAccountAdapter

from vanilla.views import FormView as VanillaFormView

from braces.views import AjaxResponseMixin, JSONResponseMixin

from avatar.views import _get_avatars
from avatar.forms import PrimaryAvatarForm, DeleteAvatarForm, UploadAvatarForm

from thoughtbubble.utils import path_and_rename
from geo.organization.models import Organization, OrganizationCurator
from geo.places.models import Place, Region
from ideation.idea.models import Idea, IdeaSupport
from forms import UserProfileForm
from models import *
from forms import SignupForm, LoginForm, OrganizationSignupForm

from django_balanced.models import Card



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

    def validate_disconnect(self, account, accounts):
        """
        Validate whether or not the socialaccount account can be
        safely disconnected.
        """
        if len(accounts) == 1:
            # No usable password would render the local account unusable
            if not account.user.has_usable_password():
                raise ValidationError(_("Your account has no password set"
                                        " up."))


def home(request):
    # if not state or not city:
    #     return redirect( reverse('home',
    #                                 args=[request.session.get('exploring_state','oh'),
    #                                             request.session.get('exploring_city','columbus'),
    #                                         ]
    #                     ))
    try:
        copy = FlatPage.objects.get(url='home').content
    except:
        copy = 'Copy here'

    d = {'copy': copy}
    return render(request, request.device_template_dir + 'home.html', d)


def logout(request):
    django_logout(request)
    return redirect('home')


def explore(request, pk=None):

    # if state:
    #     request.session['exploring_state'] = state
    #
    # if city:
    #     request.session['exploring_city'] = city

    d = {}
    #d['organizations'] = Organization.objects.filter(city__name__iexact=city, city__state_code__iexact=state).order_by('title')

    # d['metros'] = {
    #     'current': city if city else 'Columbus',
    #     'list': City.objects.none() #City.objects.values_list('name','state').distinct(),
    # }

    if pk:
        d['exploring'] = Organization.objects.get(pk=pk)

    return render(request, request.device_template_dir + 'explore.html', d)


def sherlock(request, place=None, organization=None):

    # if state:
    #     request.session['exploring_state'] = state
    #
    # if city:
    #     request.session['exploring_city'] = city

    d = {}
    # d['organizations'] = Organization.objects.filter().order_by('name')

    d['exploring'] = Organization.objects.get(place__slug__iexact=place, slug__iexact=organization)

    return render(request, request.device_template_dir + 'sherlock.html', d)


def debit_card(request):
    if request.POST:
        card_uri = request.POST.get('balancedCreditCardURI')
        card = Card.create_from_card_uri(request.user, card_uri)
        buyer = card.user.balanced_account
        # put some money in the escrow account
        r = buyer.debit(int(100 * 100), 'THOUGHTBUBBLE1')  # $100.00
        messages.add_message(request, messages.INFO, 'Thank you for your purchase.')
        return redirect('home')


    return HttpResponse('no good!')


# def thankyou(request):
#     messages.add_message(request, messages.INFO, 'Thank you for your purchase.')
#     return redirect('home')

def checkout(request):
    return render(request, request.device_template_dir + 'checkout.html', {'balanced': settings.BALANCED, 'static_url':'/static',})

def privacy(request):
    return render(request, request.device_template_dir + 'privacy.html')

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

    return render(request, request.device_template_dir + 'signup.html', {'form': form, 'captcha_answer': s['answer']})



def organization_signup(request):
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
        form = OrganizationSignupForm(request.POST, request.FILES, captcha_choices=s['choices'], answer=s['answer']) # A form bound to the POST data
        if form.is_valid():
            cleaned_data = form.cleaned_data

            # create user here
            user = ThoughtbubbleUser.objects.create_user(cleaned_data['username'],
                                                         cleaned_data['email'],
                                                         cleaned_data['password'])

            # create a new organization here
            organization = Organization()
            organization.title = cleaned_data['organization_name']
            curator = OrganizationCurator()
            curator.curator = user
            curator.save()
            organization.save()
            organization.curators.add(curator)
            organization.save()

            django_logout(request)
            user = authenticate(username=cleaned_data['username'], email= cleaned_data['email'], password=cleaned_data['password'])

            # Create initial profile for the user
            user_profile = ThoughtbubbleUserProfile.objects.create(user=user, location=cleaned_data['location'])
            if cleaned_data['profile_picture']:
                avatar = Avatar.objects.create(user=user,primary=True, avatar=cleaned_data['profile_picture'])

            django_login(request, user)
            return redirect('home')
    else:
        form = OrganizationSignupForm(captcha_choices=s['choices'], answer=s['answer'])

    return render(request, request.device_template_dir + 'organization_signup.html', {'form': form, 'captcha_answer': s['answer']})


class MyConnectionsView(FormView):
    template_name = "accounts/dashboard.html"
    form_class = DisconnectForm
    success_url = reverse_lazy("user_dashboard")

    def get_form_kwargs(self):
        kwargs = super(MyConnectionsView, self).get_form_kwargs()
        kwargs["request"] = self.request
        return kwargs

    def get_template_names(self):
        return self.request.device_template_dir + super(MyConnectionsView, self).get_template_names().pop()

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

        upload_form=UploadAvatarForm
        p_form=PrimaryAvatarForm
        avatar, avatars = _get_avatars(self.request.user)
        if avatar:
            kwargs = {'initial': {'choice': avatar.id}}
        else:
            kwargs = {}
        context['avatars'] = avatars
        upload_avatar_form = upload_form(user=self.request.user, **kwargs)
        primary_avatar_form = p_form(self.request.POST or None,
                                           avatars=avatars,
                                       user=self.request.user,
                                       **kwargs)

        context['upload_avatar_form'] = upload_avatar_form
        context['primary_avatar_form'] = primary_avatar_form

        return context


class UserProfileFormView(VanillaFormView,AjaxResponseMixin, JSONResponseMixin):
    form_class = UserProfileForm
    template_name = "accounts/update.html"

    def get_template_names(self):
        return self.request.device_template_dir + super(UserProfileFormView, self).get_template_names()


from forms import ContactForm
from django.core.mail import send_mail

class ContactFormView(VanillaFormView):
    form_class = ContactForm
    template_name = "contact.html"

    def form_valid(self, form):
        send_mail(form.cleaned_data['subject'], form.cleaned_data['body'], form.cleaned_data['email'],
                  ['blorenz@gmail.com'], fail_silently=False)
        return render(self.request, self.template_name, {'success': True})
