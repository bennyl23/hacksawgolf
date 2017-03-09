from django.views.generic import TemplateView
from django.http import HttpResponse
from golfer.models import Golfer
from tournament.models import Tournament, TournamentScoresView
from braces import views
from django.views.generic import View
from django.template.loader import render_to_string
from team.models import TeamMember
from django.utils.functional import cached_property


class ScoresView(TemplateView):
    template_name = 'tournament/scores.html'

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

    def tournament_count(self):
        return Tournament.objects.count()

    def tournament_scores(self):
        tournament = self.tournament()

        tournament_scores = TournamentScoresView.objects.filter(tournament_id=tournament.tournament_id).order_by('-tot_winnings', '-tot_winnings_for_year', 'user_team_name')

        return tournament_scores

    @cached_property
    def team_members(self):
        tournament = self.tournament()

        team_members = TeamMember.objects.filter(tournament_id=tournament.tournament_id).order_by('user_id','-salary')

        return team_members

    def current_user_id(self):
        return self.request.session['user_id']

    def team_for_tournament_for_current_user(self):
        tournament = self.tournament()

        user_team_members = TeamMember.objects.filter(
                                                      user_id=self.current_user_id(),
                                                      tournament_id=tournament.tournament_id
                                                      ).order_by(
                                                                 '-salary',
                                                                 'golfer_lname'
                                                                 )

        return user_team_members


def getDefaultSalaryForGolfer(request, golfer_id=0):
    default_salary = 'N/A'
    try:
        golfer = Golfer.objects.get(golfer_id=golfer_id)
        default_salary = golfer.default_salary
    except golfer.DoesNotExist:
        pass

    return HttpResponse(default_salary)


class GetTeamForUserForTournament(views.JSONResponseMixin, views.AjaxResponseMixin, View):

    def get_ajax(self, request, *args, **kwargs):
        response = {}

        tournament = Tournament.objects.get(tournament_id=int(self.kwargs['tournament_id']))

        user_team_members = TeamMember.objects.filter(
                                                      user_id=int(self.kwargs['user_id']),
                                                      tournament_id=int(self.kwargs['tournament_id'])
                                                      ).order_by(
                                                                 '-salary',
                                                                 'golfer_lname'
                                                                 )

        team_html = render_to_string('tournament/user_team_for_tournament.html', {
                                                                                  'team_members': user_team_members,
                                                                                  'tournament': tournament
                                                                                  })

        response['team_html'] = team_html

        return self.render_json_response(response)
