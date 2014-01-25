from django import template

import allauth.socialaccount.providers as providers

register = template.Library()

@register.filter(name='get_provider')
def get_provider(value):
    return providers

