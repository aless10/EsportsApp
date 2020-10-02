from rest_framework import serializers

from .models import Match, Team, Tournament, Score, Event


class MatchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Match
        fields = '__all__'


class TeamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Team
        fields = '__all__'


class TournamentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tournament
        fields = '__all__'


class ScoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Score
        fields = '__all__'


class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = '__all__'
