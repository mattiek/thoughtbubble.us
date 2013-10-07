from forms import SignupForm, LoginForm
from thoughtbubble.settings import DOMAIN_HOST
def login_form(request):
    d = {'loginform': LoginForm(),}
    return d

def domain_host(request):
    d = {'DOMAIN_HOST': DOMAIN_HOST}
    return d
