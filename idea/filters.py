import django_filters
from models import Idea

class IdeaFilter(django_filters.FilterSet):
    # most_supported = django_filters.NumberFilter(lookup_type='lt')
    date_created = django_filters.DateRangeFilter()
    class Meta:
        model = Idea
        fields = ['where', 'date_created']


# class IdeaOrdering(object):
