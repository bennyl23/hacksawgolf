from django.db import models
from golfer.models import Golfer
import datetime
from django.core.exceptions import ValidationError
from django.core.exceptions import ObjectDoesNotExist
from django.utils import timezone


# tournament model manager
class TournamentsManager(models.Manager):
    def current_tournament(self):
        """Return a tournament model instance for the current week"""
        try:
            tournament = Tournament.objects.get(
                start_date__lte=datetime.datetime.now(),
                end_date__gte=datetime.datetime.now()
            )
        except Tournament.DoesNotExist:
            tournament = Tournament.objects.get(tournament_week=1)

        return tournament


class TournamentType(models.Model):
    tournament_type_id = models.AutoField(primary_key=True)
    tournament_type = models.CharField(max_length=50, blank=False)
    tournament_type_five_mdc = models.IntegerField(default=0, blank=False)
    tournament_type_six_mdc = models.IntegerField(default=0, blank=False)
    tournament_type_winnings_multiplier = models.DecimalField(default=1, blank=False, max_digits=3, decimal_places=2)

    class Meta:
        db_table = 'tournament_type_t'

    def __unicode__(self):
        return unicode(str(self.tournament_type))


class Tournament(models.Model):
    tournament_id = models.AutoField(primary_key=True)
    tournament_name = models.CharField(max_length=255)
    tournament_location = models.CharField(max_length=255)
    tournament_abbrv = models.CharField(max_length=20)
    tournament_week = models.IntegerField()
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    tournament_type = models.ForeignKey(TournamentType)
    tournament_winner = models.ForeignKey('register.User', related_name='tournament_winner_user_id', db_column='tournament_winner', blank=True, null=True)
    tournament_winnings = models.CharField(verbose_name='1st winnings', max_length=10)
    anyone = models.CharField(verbose_name='Winner gets', max_length=20)
    multiwin = models.CharField(verbose_name='Multiwin gets', max_length=20)
    in_contention = models.IntegerField(verbose_name='In contention STP')
    cut_point = models.BooleanField(default=False)
    ready_for_picks = models.BooleanField(default=False)
    tournament_second_place = models.ForeignKey('register.User', related_name='tournament_second_place_user_id', db_column='tournament_second_place', blank=True, null=True)
    tournament_second_place_winnings = models.CharField(verbose_name='2nd gets', max_length=10)

    picks_lock_date = models.DateTimeField()
    objects = TournamentsManager()

    class Meta:
        db_table = 'tournament_t'

    def __unicode__(self):
        return unicode(self.tournament_name)

    def tournament_locked(self):
        if self.picks_lock_date <= timezone.now():
            return True

        return False

    def in_contention_converted(self):
        if self.in_contention is not None:
            if self.in_contention == 0:
                return 'ev'
            elif self.in_contention > 0:
                return '+' + str(self.in_contention)

            return str(self.in_contention)

        return 'N/A'


class TournamentParticipant(models.Model):
    tournament_participant_id = models.AutoField(primary_key=True)
    golfer = models.ForeignKey(Golfer)
    tournament = models.ForeignKey(Tournament)
    salary = models.IntegerField()
    score_to_par = models.IntegerField(blank=True, null=True)
    winnings = models.IntegerField(default=0)
    status = models.CharField(max_length=5, blank=True)
    made_the_cut = models.BooleanField(default=False)

    class Meta:
        db_table = 'tournament_participant_t'

    def __unicode__(self):
        return unicode(str(self.tournament_id) + ', ' + str(self.golfer_id))

    def clean(self, *args, **kwargs):
        try:
            # only check when creating new tournament_participant, not updating
            if self.pk is None:
                golfer_in_tournament = TournamentParticipant.objects.filter(tournament_id=self.tournament_id, golfer_id=self.golfer_id)
                if golfer_in_tournament:
                    raise ValidationError('The golfer you selected has already been added to this tournament.')
        except ObjectDoesNotExist:
            pass


class TournamentParticipantView(models.Model):
    tournament_participant_id = models.IntegerField(primary_key=True)
    golfer_id = models.IntegerField()
    tournament_id = models.IntegerField()
    salary = models.IntegerField()
    score_to_par = models.IntegerField()
    winnings = models.IntegerField()
    status = models.CharField(max_length=5)
    made_the_cut = models.BooleanField(default=False)
    golfer_fname = models.CharField(max_length=50)
    golfer_lname = models.CharField(max_length=50)
    golfer_mi = models.CharField(max_length=10)
    golfer_fname_initial = models.CharField(max_length=1)

    class Meta:
        managed = False
        db_table = 'tournament_participant_v'


class TournamentScoresView(models.Model):
    user_id = models.IntegerField(primary_key=True)
    tournament_id = models.IntegerField()
    user_team_name = models.CharField(max_length=20)
    user_bonus = models.IntegerField()
    winnings = models.IntegerField()
    tournament_week = models.IntegerField()
    tournament_name = models.CharField(max_length=255)
    tot_winnings = models.IntegerField()
    mtc_count = models.IntegerField()
    tot_winnings_for_year = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'tournament_scores_v'
