from forms import SignupForm, LoginForm
from thoughtbubble.settings import DOMAIN_HOST
from cities.models import City

def login_form(request):
    d = {'loginform': LoginForm(),}
    return d

def domain_host(request):
    d = {'DOMAIN_HOST': DOMAIN_HOST}
    return d

def exploring(request):
    city = request.session.get('exploring_city', None)
    state =  request.session.get('exploring_state', None)

    if not city or not state:
        city = 'Columbus'
        state = 'OH'

    obj = City.objects.filter(name__iexact=city, state_code__iexact=state)
    if obj:
        obj = obj[0]
    d = {

        'exploring_city': city.lower(),
        'exploring_state': state.lower(),
        'exploring_obj' : obj
    }
    return d
