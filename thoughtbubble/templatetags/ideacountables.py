from django import template
from idea.models import Idea, IdeaSupport
from community.models import Community


register = template.Library()

@register.filter(name='idea_count')
def idea_count(value):
    return Idea.objects.filter(user=value).count()

@register.filter(name='idea_support_count')
def get_idea_support_count(value):
    return IdeaSupport.objects.filter(user=value).count()

@register.filter(name='communities_joined_count')
def get_idea_support_count(value):
    return Community.objects.filter(members=value).count()