from django import template
from idea.models import Idea, IdeaSupport
from community.models import Community
from supportering.models import CommentSupport

register = template.Library()

@register.filter(name='idea_count')
def idea_count(value):
    return Idea.objects.filter(user=value).count()

@register.filter(name='idea_support_count')
def get_idea_support_count(value):
    return IdeaSupport.objects.filter(user=value).count()

@register.filter(name='communities_joined_count')
def communities_joined_count(value):
    return Community.objects.filter(members=value).count()

@register.filter(name='is_supported_by_user')
def is_supported(value, arg):
    if not arg.is_authenticated():
        return False
    return IdeaSupport.objects.filter(user=arg, idea=value).count()

@register.filter(name='comment_support_count')
def comment_support_count(value):
    return CommentSupport.objects.filter(comment=value).count()