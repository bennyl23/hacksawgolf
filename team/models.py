from django.db import models
from team.models_helpers import score_to_par_converted, status_converted


class Team(models.Model):
    team_id = models.AutoField(primary_key=True)
    user = models.ForeignKey('register.User', db_column='user_id')
    tournament = models.ForeignKey('tournament.Tournament', db_column='tournament_id')
    golfer = models.ForeignKey('golfer.Golfer', db_column='golfer_id')

    class Meta:
        db_table = 'team_t'

    def __unicode__(self):
        return unicode(self.team_id)

class TeamMember(models.Model):
    team_id = models.IntegerField(primary_key=True)
    user_id = models.IntegerField()
    user_team_name = models.CharField(max_length=20)
    golfer_id = models.IntegerField()
    golfer_fname = models.CharField(max_length=50)
    golfer_lname = models.CharField(max_length=50)
    golfer_mi = models.CharField(max_length=10)
    golfer_fname_initial = models.CharField(max_length=1)
    tournament_id = models.IntegerField()
    salary = models.IntegerField()
    score_to_par = models.IntegerField()
    winnings = models.IntegerField()
    status = models.CharField(max_length=5)
    made_the_cut = models.IntegerField()
    times_picked = models.IntegerField()
    cut_point = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'team_v'

    def score_to_par_converted(self):
        return score_to_par_converted(self.score_to_par)

    def status_converted(self):
        return status_converted(self.status, self.cut_point, self.made_the_cut)
