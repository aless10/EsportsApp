from django.urls import path

from .views import MatchView

urlpatterns = [
    path(
        r'matches',
        MatchView.as_view({'get': 'list'}),
        name='match-list-view'),
    path(
        r'matches/<int:pk>',
        MatchView.as_view({'get': 'retrieve'}),
        name='match-detail-view'),
]
