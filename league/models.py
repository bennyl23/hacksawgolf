from django.db import models
from team.models_helpers import score_to_par_converted, status_converted


class Standings(models.Model):
    user_id = models.IntegerField(primary_key=True)
    user_team_name = models.CharField(max_length=20)
    tot_winnings = models.IntegerField()
    user_wins = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'standings_v'


class Breakdown(models.Model):
    tournament_participant_id = models.IntegerField(primary_key=True)
    golfer_id = models.IntegerField()
    tournament_id = models.IntegerField()
    salary = models.IntegerField()
    score_to_par = models.IntegerField()
    winnings = models.IntegerField()
    status = models.CharField(max_length=5)
    golfer_fname = models.CharField(max_length=50)
    golfer_lname = models.CharField(max_length=50)
    golfer_mi = models.CharField(max_length=10)
    golfer_fname_initial = models.CharField(max_length=1)
    made_the_cut = models.IntegerField()
    times_picked = models.IntegerField()
    cut_point = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'tournament_breakdown_v'

    def score_to_par_converted(self):
        return score_to_par_converted(self.score_to_par)

    def status_converted(self):
        return status_converted(self.status, self.cut_point, self.made_the_cut)

