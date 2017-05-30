from django.views.generic import TemplateView, ListView, FormView
from league.models import Standings, Breakdown
from tournament.models import TournamentScoresView
from register.models import User
from tournament.models import Tournament
from team.models import Team
from league.forms import TeamCompareForm
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


class TeamCompareView(FormView):
    template_name = 'league/team_compare.html'
    form_class = TeamCompareForm

    # set initial values on the form with data not available in the form's model
    def get_initial(self):
        initial = super(TeamCompareView, self).get_initial()
        initial['team_one_compare'] = self.request.session['user_id']
        return initial

    # override the form_valid method
    def form_valid(self, form):
        context = self.get_context_data(form=form)

        # get selected teams' user ids
        team_one_user_id = form.cleaned_data['team_one_compare'].user_id
        team_two_user_id = form.cleaned_data['team_two_compare'].user_id

        team_one_scores = TournamentScoresView.objects.filter(
                                                              user_id=int(team_one_user_id)
                                                              ).order_by(
                                                                         'tournament_week'
                                                                         )
        team_two_scores = TournamentScoresView.objects.filter(
                                                              user_id=int(team_two_user_id)
                                                              ).order_by(
                                                                         'tournament_week'
                                                                         )
        team_compare_list = []
        team_one_user = User.objects.get(user_id=team_one_user_id)
        team_two_user = User.objects.get(user_id=team_two_user_id)

        team_one_wins = 0
        team_two_wins = 0
        ties = 0
        team_one_better = False
        team_two_better = False
        team_compare_error = ''

        for team_one_score in team_one_scores:
            team_compare_dict = {}

            try:
                team_two_score = team_two_scores.get(tournament_id=team_one_score.tournament_id)
            except:
                # if there was an getting a matching score for team two, send back an error
                team_compare_error = 'There was a problem comparing teams.  One of the selected teams may have missed a tournament.'
                break

            team_compare_dict['tournament_name'] = team_one_score.tournament_name
            team_compare_dict['tournament_abbrv'] = team_one_score.tournament_abbrv
            team_compare_dict['team_one_score'] = team_one_score.tot_winnings
            team_compare_dict['team_two_score'] = team_two_score.tot_winnings
            team_compare_dict['team_one_winner'] = False
            team_compare_dict['team_two_winner'] = False
            team_compare_dict['tie'] = False
            if team_one_score.tot_winnings > team_two_score.tot_winnings:
                team_compare_dict['team_one_winner'] = True
                team_one_wins += 1
            elif team_two_score.tot_winnings > team_one_score.tot_winnings:
                team_compare_dict['team_two_winner'] = True
                team_two_wins += 1
            else:
                team_compare_dict['tie'] = True
                ties += 1

            team_compare_list.append(team_compare_dict)


        if team_one_wins > team_two_wins:
            team_one_better = True

        if team_two_wins > team_one_wins:
            team_two_better = True

        context['team_compare_list'] = team_compare_list
        context['team_one_user'] = team_one_user
        context['team_two_user'] = team_two_user
        context['team_one_wins'] = team_one_wins
        context['team_two_wins'] = team_two_wins
        context['ties'] = ties
        context['team_one_better'] = team_one_better
        context['team_two_better'] = team_two_better
        context['team_compare_error'] = team_compare_error

        return self.render_to_response(context)
