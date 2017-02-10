from django.views.generic import TemplateView
from tournament.models import Tournament, TournamentParticipant, TournamentParticipantView
from team.models import TeamMember, Team
from django.db.models import Sum
from braces import views
from django.views.generic import View
from django.template.loader import render_to_string
from team.functions import delete_team


class TeamView(TemplateView):
    template_name = 'team/team.html'

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

    def tournament_participants(self):
        tournament = self.tournament()

        return TournamentParticipant.objects.filter(tournament__tournament_id=tournament.tournament_id).order_by('-salary', 'golfer__golfer_lname')

    def team(self):
        response = {}

        tournament = self.tournament()

        # check if user is editing their team, if so, check for a selected team in session
        if '/edit/' in self.request.path and 'selected_golfers' in self.request.session and self.request.session['selected_golfers']:
            '''
                Using the selected golfer list in session here.  They have not been saved yet so they are not in the team_t table.
                Create a queryset from the TournamentParticipantView model to mirror what the TeamMember model looks like.
                If the TournamentParticipant model was used, the template would need to use foreign key evaluators to
                access the foreign key table data, whereas the TeamMember model is a sql view and already has the foreign key
                data.
            '''
            team_members = TournamentParticipantView.objects.filter(
                                                                    tournament_id=tournament.tournament_id,
                                                                    golfer_id__in=self.request.session['selected_golfers']
                                                                    ).order_by(
                                                                               '-salary',
                                                                               'golfer_lname'
                                                                               )
        # if no selected team in session, get the selected team from the TeamMember model
        else:
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
        response['team_member_list'] = team_members.values_list('golfer_id', flat=True)

        return response


class GetGolferForTournament(views.JSONResponseMixin, views.AjaxResponseMixin, View):

    def get_ajax(self, request, *args, **kwargs):
        tournamentParticipant = TournamentParticipant.objects.get(
                                                                  tournament_id=int(self.kwargs['tournament_id']),
                                                                  golfer_id=int(self.kwargs['golfer_id'])
                                                                  )
        golfer_dict = {
                         'golfer_id': tournamentParticipant.golfer.golfer_id,
                         'golfer_fname': tournamentParticipant.golfer.golfer_fname,
                         'golfer_lname': tournamentParticipant.golfer.golfer_lname,
                         'golfer_fname_initial': tournamentParticipant.golfer.golfer_fname[:1],
                         'salary': tournamentParticipant.salary,
                         'golfer_html': ''
                         }

        golfer_html = render_to_string('team/team_member.html', {
                                                                 'team_member': golfer_dict,
                                                                 'counter': self.kwargs['counter']
                                                                 })

        golfer_dict['golfer_html'] = golfer_html;

        return self.render_json_response(golfer_dict)


class ValidateTeamSelect(views.JsonRequestResponseMixin, View):

    def post(self, request, *args, **kwargs):
        response = {}
        response['successful'] = True;

        team_dict = self.request_json;
        selected_golfers = team_dict['selected_golfers'];

        # did not select 6 golfers (this shouldn't happen but check for it anyway)
        if len(selected_golfers) != 6:
            response['successful'] = False;
            response['error'] = 'You must select exactly 6 golfers.'

        # salary is greater than 250
        salary_total = 0
        for golfer in selected_golfers:
            salary_total += golfer['golfer_salary']
        if salary_total > 250:
            response['successful'] = False;
            response['error'] = 'Total salary must be 250 or less.'

        return self.render_json_response(response)


class VerifyTeamView(TemplateView):
    template_name = 'team/team_verify.html'

    # override the post method on the templateview
    def post(self, request, *args, **kwargs):
        context = self.get_context_data();

        golfer_ids = []
        # loop over the submitted form data and create a list of the selected golfer_id's
        for key, value in context["form"].items():
            if key.startswith('selected_golfer_id_'):
                golfer_ids.append(value)

        tournament_id = context['form']['tournament_id']

        # get the golfers from the db and add them to the context
        selected_golfers = TournamentParticipant.objects.filter(
                                                       tournament__tournament_id=tournament_id,
                                                       golfer__golfer_id__in=golfer_ids
                                                       ).order_by (
                                                                   '-salary',
                                                                   'golfer__golfer_lname'
                                                                   )

        # put a list of the selected golfers in session
        self.request.session['selected_golfers'] = selected_golfers.values_list('golfer__golfer_id', flat=True)

        # sum up the salary of the selected golfers
        salary_total = selected_golfers.aggregate(Sum('salary'))

        # get the tournament
        tournament = Tournament.objects.get(tournament_id=tournament_id)

        # add data to the context
        context['tournament'] = tournament
        context['selected_golfers'] = selected_golfers
        context['salary_total'] = salary_total

        return super(TemplateView, self).render_to_response(context);

    # override the get_context_data method to extract the POST data
    def get_context_data(self, **kwargs):
        context = super(VerifyTeamView, self).get_context_data(**kwargs)

        context["form"] = self.request.POST

        return context


class SaveTeamView(views.JsonRequestResponseMixin, View):

    def post(self, request, *args, **kwargs):
        response = {}
        response['successful'] = True;

        user_id = self.request.session['user_id']
        tournament_id = self.request_json['tournament_id']

        # delete any previous selections this user has made for this tournament
        delete_team(user_id, tournament_id)

        # get the user's selections from session
        selected_golfer_list = self.request.session['selected_golfers']

        # loop over the selected_golfer_list, create a new team model object and save the team
        for golfer_id in selected_golfer_list:
            team_new = Team(
                            user_id = user_id,
                            tournament_id = tournament_id,
                            golfer_id = golfer_id
                            )
            try:
                team_new.save()
            except:
                # if there was an error during save, delete all db rows for this user for this tournament
                delete_team(user_id, tournament_id)
                response['successful'] = False;
                response['error'] = 'There was a problem saving your team.  Please try again.'
                break

        return self.render_json_response(response)
