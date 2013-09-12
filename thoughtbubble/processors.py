from forms import SignupForm, LoginForm

def login_form(request):
    d = {'loginform': LoginForm(),}
    return d
