from django import template

register = template.Library()

@register.filter(name='getdict')
def getdict(value,arg):
    d = None
    try:
        d = value[arg]
    except:
        pass
    return d