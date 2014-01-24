from django import template
from ideation.idea.models import Idea, IdeaSupport
from geo.organization.models import Organization
from ideation.supportering.models import CommentSupport

register = template.Library()

@register.filter(name='idea_count')
def idea_count(value):
    if not value.is_authenticated():
        return 0
    return Idea.objects.filter(user=value).count()

@register.filter(name='idea_support_count')
def get_idea_support_count(value):
    if not value.is_authenticated():
        return 0
    return IdeaSupport.objects.filter(user=value).count()

@register.filter(name='organizations_joined_count')
def organizations_joined_count(value):
    if not value.is_authenticated():
        return 0
    return Organization.objects.filter(members=value).count()

@register.filter(name='is_supported_by_user')
def is_supported(value, arg):
    if not arg.is_authenticated():
        return False
    return IdeaSupport.objects.filter(user=arg, idea=value).count()

@register.filter(name='comment_support_count')
def comment_support_count(value):
    return CommentSupport.objects.filter(comment=value).count()