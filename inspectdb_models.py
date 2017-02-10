# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Remove `managed = False` lines for those models you wish to give write DB access
# Feel free to rename the models, but don't rename db_table values or field names.
#
# Also note: You'll have to insert the output of 'django-admin.py sqlcustom [appname]'
# into your database.
from __future__ import unicode_literals

from django.db import models

class AuthGroup(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(unique=True, max_length=80)
    class Meta:
        managed = False
        db_table = 'auth_group'

class AuthGroupPermissions(models.Model):
    id = models.IntegerField(primary_key=True)
    group = models.ForeignKey(AuthGroup)
    permission = models.ForeignKey('AuthPermission')
    class Meta:
        managed = False
        db_table = 'auth_group_permissions'

class AuthPermission(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=50)
    content_type = models.ForeignKey('DjangoContentType')
    codename = models.CharField(max_length=100)
    class Meta:
        managed = False
        db_table = 'auth_permission'

class AuthUser(models.Model):
    id = models.IntegerField(primary_key=True)
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField()
    is_superuser = models.IntegerField()
    username = models.CharField(unique=True, max_length=30)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    email = models.CharField(max_length=75)
    is_staff = models.IntegerField()
    is_active = models.IntegerField()
    date_joined = models.DateTimeField()
    class Meta:
        managed = False
        db_table = 'auth_user'

class AuthUserGroups(models.Model):
    id = models.IntegerField(primary_key=True)
    user = models.ForeignKey(AuthUser)
    group = models.ForeignKey(AuthGroup)
    class Meta:
        managed = False
        db_table = 'auth_user_groups'

class AuthUserUserPermissions(models.Model):
    id = models.IntegerField(primary_key=True)
    user = models.ForeignKey(AuthUser)
    permission = models.ForeignKey(AuthPermission)
    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'

class CalcBonusV(models.Model):
    user_id = models.IntegerField()
    user_team_name = models.CharField(max_length=20)
    tournament_id = models.IntegerField()
    tournament_type = models.CharField(max_length=15)
    winnings = models.DecimalField(max_digits=30, decimal_places=0, blank=True, null=True)
    mtc_count = models.DecimalField(max_digits=25, decimal_places=0, blank=True, null=True)
    user_win = models.IntegerField()
    user_bonus = models.BigIntegerField(blank=True, null=True)
    class Meta:
        managed = False
        db_table = 'calc_bonus_v'

class CutsMadeV(models.Model):
    user_id = models.IntegerField()
    user_team_name = models.CharField(max_length=20)
    tournament_id = models.IntegerField()
    tournament_type = models.CharField(max_length=15)
    tournament_winner = models.IntegerField()
    winnings = models.DecimalField(max_digits=30, decimal_places=0, blank=True, null=True)
    mtc_count = models.DecimalField(max_digits=25, decimal_places=0, blank=True, null=True)
    user_win = models.IntegerField()
    class Meta:
        managed = False
        db_table = 'cuts_made_v'

class DjangoAdminLog(models.Model):
    id = models.IntegerField(primary_key=True)
    action_time = models.DateTimeField()
    user = models.ForeignKey(AuthUser)
    content_type = models.ForeignKey('DjangoContentType', blank=True, null=True)
    object_id = models.TextField(blank=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.IntegerField()
    change_message = models.TextField()
    class Meta:
        managed = False
        db_table = 'django_admin_log'

class DjangoContentType(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=100)
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)
    class Meta:
        managed = False
        db_table = 'django_content_type'

class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()
    class Meta:
        managed = False
        db_table = 'django_session'

class GolferT(models.Model):
    golfer_id = models.IntegerField(primary_key=True)
    golfer_fname = models.CharField(max_length=50)
    golfer_lname = models.CharField(max_length=50)
    golfer_mi = models.CharField(max_length=10, blank=True)
    default_salary = models.IntegerField()
    original_salary = models.IntegerField(blank=True, null=True)
    class Meta:
        managed = False
        db_table = 'golfer_t'

class OverallScoresV(models.Model):
    user_id = models.IntegerField()
    user_team_name = models.CharField(max_length=20)
    tot_winnings = models.DecimalField(max_digits=53, decimal_places=0, blank=True, null=True)
    user_wins = models.DecimalField(max_digits=32, decimal_places=0, blank=True, null=True)
    class Meta:
        managed = False
        db_table = 'overall_scores_v'

class ScoresV(models.Model):
    user_id = models.IntegerField()
    user_team_name = models.CharField(max_length=20)
    tournament_id = models.IntegerField()
    tournament_abbrv = models.CharField(max_length=20)
    tournament_name = models.CharField(max_length=255)
    tournament_week = models.IntegerField()
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    tournament_type = models.CharField(max_length=15)
    tournament_winner = models.IntegerField()
    cut_point = models.IntegerField()
    golfer_id = models.IntegerField()
    golfer_fname = models.CharField(db_column='golfer_fName', max_length=50) # Field name made lowercase.
    golfer_lname = models.CharField(db_column='golfer_lName', max_length=50) # Field name made lowercase.
    golfer_mi = models.CharField(max_length=10, blank=True)
    salary = models.IntegerField()
    score_to_par = models.IntegerField(blank=True, null=True)
    status = models.CharField(max_length=5, blank=True)
    winnings = models.IntegerField()
    orig_winnings = models.IntegerField()
    made_the_cut = models.IntegerField()
    times_golfer_picked = models.BigIntegerField(blank=True, null=True)
    class Meta:
        managed = False
        db_table = 'scores_v'

class TeamT(models.Model):
    team_id = models.IntegerField(primary_key=True)
    user = models.ForeignKey('UserT')
    tournament = models.ForeignKey('TournamentT')
    golfer = models.ForeignKey(GolferT)
    class Meta:
        managed = False
        db_table = 'team_t'

class TeamV(models.Model):
    team_id = models.IntegerField()
    user_id = models.IntegerField()
    user_team_name = models.CharField(max_length=20)
    golfer_id = models.IntegerField()
    golfer_fname = models.CharField(max_length=50)
    golfer_lname = models.CharField(max_length=50)
    golfer_mi = models.CharField(max_length=10, blank=True)
    tournament_id = models.IntegerField()
    salary = models.IntegerField()
    score_to_par = models.IntegerField(blank=True, null=True)
    winnings = models.IntegerField()
    status = models.CharField(max_length=5, blank=True)
    made_the_cut = models.IntegerField()
    class Meta:
        managed = False
        db_table = 'team_v'

class TournamentParticipantT(models.Model):
    tournament_participant_id = models.IntegerField(primary_key=True)
    tournament = models.ForeignKey('TournamentT')
    golfer = models.ForeignKey(GolferT)
    salary = models.IntegerField()
    score_to_par = models.IntegerField(blank=True, null=True)
    winnings = models.IntegerField()
    orig_winnings = models.IntegerField()
    status = models.CharField(max_length=5, blank=True)
    made_the_cut = models.IntegerField()
    class Meta:
        managed = False
        db_table = 'tournament_participant_t'

class TournamentScoresV(models.Model):
    user_id = models.IntegerField()
    tournament_id = models.IntegerField()
    user_team_name = models.CharField(max_length=20)
    user_bonus = models.IntegerField(blank=True, null=True)
    winnings = models.DecimalField(max_digits=30, decimal_places=0, blank=True, null=True)
    tournament_week = models.IntegerField()
    tournament_name = models.CharField(max_length=255)
    tot_winnings = models.DecimalField(max_digits=53, decimal_places=0, blank=True, null=True)
    class Meta:
        managed = False
        db_table = 'tournament_scores_v'

class TournamentT(models.Model):
    tournament_id = models.IntegerField(primary_key=True)
    tournament_name = models.CharField(max_length=255)
    tournament_abbrv = models.CharField(max_length=20)
    tournament_week = models.IntegerField()
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    tournament_type = models.CharField(max_length=15)
    tournament_winner = models.IntegerField()
    tournament_winnings = models.CharField(max_length=10)
    anyone = models.CharField(max_length=20)
    multiwin = models.CharField(max_length=20)
    in_contention = models.IntegerField()
    cut_point = models.IntegerField()
    ready_for_picks = models.IntegerField()
    tournament_second_place = models.IntegerField(blank=True, null=True)
    tournament_location = models.CharField(max_length=255)
    class Meta:
        managed = False
        db_table = 'tournament_t'

class UserT(models.Model):
    user_id = models.IntegerField(primary_key=True)
    user_email = models.CharField(max_length=50)
    user_password = models.CharField(max_length=128)
    user_team_name = models.CharField(max_length=20)
    user_referring_email = models.CharField(max_length=50)
    user_af1 = models.CharField(max_length=30, blank=True)
    user_af2 = models.CharField(max_length=30, blank=True)
    user_real_name = models.CharField(max_length=50, blank=True)
    user_paid = models.IntegerField(blank=True, null=True)
    message_from_commish = models.TextField(blank=True)
    class Meta:
        managed = False
        db_table = 'user_t'

