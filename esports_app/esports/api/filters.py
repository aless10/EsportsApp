from django_filters import FilterSet

from .models import Match


class MatchFilter(FilterSet):
    class Meta:
        model = Match
        fields = {
            'title': ['exact'],
            'tournament': ['exact'],
            'state': ['exact'],
            'date_start': ['gte', 'lte'],
        }
