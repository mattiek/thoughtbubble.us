from django import template
from idea.models import Idea, IdeaSupport


register = template.Library()

@register.filter(name='idea_count')
def idea_count(value):
    return Idea.objects.filter(user=value).count()
#
# def get_idea_support_count(self):
#     return IdeaSupport.objects.filter(user=self.user).count()