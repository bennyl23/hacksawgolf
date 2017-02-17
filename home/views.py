from django.views.generic import TemplateView
from tournament.models import Tournament
from register.models import User
from team.models import TeamMember
from django.db.models import Sum
from home.models import Blog


class HomeView(TemplateView):
    template_name = 'home/home.html'

    def user(self):
        return User.objects.get(user_id=self.request.session['user_id'])

    def tournament(self):
        # if user is navigating to a specific tournament (e.g. /home/4/)
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

    def team(self):
        response = {}

        tournament = self.tournament()

        team_members = TeamMember.objects.filter(
                                                     user_id=self.request.session['user_id'],
                                                     tournament_id=tournament.tournament_id,
                                                     ).order_by(
                                                                '-salary',
                                                                'golfer_lname'
                                                                )

        salary_total = team_members.aggregate(Sum('salary'))

        response['team_members'] = team_members
        response['salary_total'] = salary_total

        return response

    def blog(self):
        return Blog.objects.all().order_by('-entry_date')