from django.db import models

# Title
# Tournament
# Team
# Match
# Scores of a Team in a Match


class Event(models.Model):
    source = models.CharField(max_length=255)
    data = models.JSONField()


class Match(models.Model):
    match_id = models.IntegerField()
    state = models.IntegerField()
    title = models.CharField(max_length=255)
    a_team_score = models.ForeignKey(
        "Score",
        on_delete=models.CASCADE,
        related_name="a_team"
    )
    b_team_score = models.ForeignKey(
        "Score",
        on_delete=models.CASCADE,
        related_name="b_team")
    best_of = models.IntegerField(null=True)
    date_start = models.DateTimeField()
    url = models.CharField(max_length=255)
    tournament = models.ForeignKey("Tournament", on_delete=models.CASCADE)


class Score(models.Model):
    match_id = models.IntegerField(db_index=True)
    state = models.IntegerField(null=True)
    team = models.ForeignKey("Team", on_delete=models.CASCADE)
    score = models.IntegerField(null=True)
    is_winner = models.IntegerField(null=True)
    date_start = models.DateTimeField(auto_now=True)


class Team(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=255)


class Tournament(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=255)
