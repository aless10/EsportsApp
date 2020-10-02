from rest_framework import viewsets
from django_filters import rest_framework as filters
from rest_framework.response import Response

from .filters import MatchFilter
from .models import Match
from .serializers import MatchSerializer


class MatchView(viewsets.ViewSet):
    queryset = Match.objects.all()  # pylint:disable=E1101
    serializer_class = MatchSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = MatchFilter

    def get_queryset(self):
        queryset = self._filter_qs()
        return queryset.qs

    def _filter_qs(self):
        return self.filterset_class(
            self.request.GET,
            queryset=self.queryset
        )

    def list(self, request):
        queryset = self.get_queryset()
        serialized = self.serializer_class(queryset, many=True)
        return Response(serialized.data)

    def retrieve(self, request, pk=None):
        queryset = self.queryset.get_or_404(id=pk)
        serialized = self.serializer_class(queryset)
        return Response(serialized.data)
