from django.contrib import admin

from api.models import Match, Tournament, Score, Team, Event


class MatchAdmin(admin.ModelAdmin):
    pass


class TournamentAdmin(admin.ModelAdmin):
    pass


class ScoreAdmin(admin.ModelAdmin):
    pass


class TeamAdmin(admin.ModelAdmin):
    pass


class EventAdmin(admin.ModelAdmin):
    pass


admin.site.register(Match, MatchAdmin)
admin.site.register(Tournament, TournamentAdmin)
admin.site.register(Score, ScoreAdmin)
admin.site.register(Team, TeamAdmin)
admin.site.register(Event, EventAdmin)
