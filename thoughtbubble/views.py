from django.shortcuts import render

from forms import SignupForm

def home(request):
    return render(request, 'home.html')

def signup(request):
    form = SignupForm(captcha_choices=(
                    ('a','guitarist.png'),
                    ('a','hot-dog-truck.png'),
                    ('a','jimmy-the-dinosaur.png'),
    ))

    return render(request, 'signup.html', {'form': form})