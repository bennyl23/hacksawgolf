from django.views.generic import TemplateView, ListView
from league.models import Standings, Breakdown
from tournament.models import TournamentScoresView
from register.models import User
from tournament.models import Tournament
from team.models import Team
from django.utils.functional import cached_property


class StandingsView(TemplateView):
    template_name = 'league/standings.html'

    def standings(self):
        return Standings.objects.all().order_by('-tot_winnings', 'user_team_name')

    def current_user_id(self):
        return self.request.session['user_id']


class StandingsDetailView(TemplateView):
    template_name = 'league/standings_detail.html'

    def standings_detail(self):
        return TournamentScoresView.objects.filter(user_id=int(self.kwargs['user_id'])).order_by('tournament_week')

    def user(self):
        return User.objects.get(user_id=int(self.kwargs['user_id']))


class BreakdownView(TemplateView):
    template_name = 'league/breakdown.html'

    def tournament(self):
        # if user is navigating to a specific tournament (e.g. /team/4/)
        if 'tournament_week' in self.kwargs:
            try:
                tournament = Tournament.objects.get(tournament_week=int(self.kwargs['tournament_week']))
            except Tournament.DoesNotExist:
                tournament = Tournament.objects.current_tournament()
            finally:
                return tournament
        # default to current tournament
        else:
            return Tournament.objects.current_tournament()

    def breakdown(self):
        tournament = self.tournament()

        return Breakdown.objects.filter(tournament_id=tournament.tournament_id).order_by('-times_picked', 'golfer_lname')


    @cached_property
    def current_user_team(self):
        tournament = self.tournament()

        current_user_team = Team.objects.filter(
                                                tournament__tournament_id=tournament.tournament_id,
                                                user__user_id=int(self.request.session['user_id'])
                                                )

        return current_user_team.values_list('golfer_id', flat=True)


class TournamentListView(ListView):
    context_object_name = 'tournaments'
    queryset = Tournament.objects.all().order_by('tournament_week')
    template_name = 'league/tournament_list.html'
