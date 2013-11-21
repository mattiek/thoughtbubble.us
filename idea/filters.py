import django_filters
from models import Idea
from location.models import Location

class IdeaFilter(django_filters.FilterSet):
    # most_supported = django_filters.NumberFilter(lookup_type='lt')
    date_created = django_filters.DateRangeFilter()
    class Meta:
        model = Idea
        fields = [ 'date_created']

    def __init__(self, *args, **kwargs):
        city = kwargs.pop('city','columbus')
        state = kwargs.pop('state','oh')
        super(IdeaFilter, self).__init__(*args, **kwargs)
        self.filters['content_object'].extra.update(
            {'empty_label': 'content_object',
             'queryset': Location.objects.filter(organization__neighborhood__city__iexact=city, organization__neighborhood__state__iexact=state)})
        # self.filters['date_created'].extra.update(
        #     {'empty_label': 'when'})


# class IdeaOrdering(object):
