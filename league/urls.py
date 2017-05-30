from django.conf.urls import patterns, url
from league import views
from login.functions import signed_in_only


urlpatterns = patterns('',
    # /league/standings/
    url(r'^standings/$', signed_in_only(views.StandingsView.as_view()), name='standings'),
    # /league/standings/5/
    url(r'^standings/(?P<user_id>\d+)/$', signed_in_only(views.StandingsDetailView.as_view()), name='standings_detail'),
    # /league/breakdown/
    url(r'^breakdown/$', signed_in_only(views.BreakdownView.as_view()), name='breakdown'),
    # /league/breakdown/14/
    url(r'^breakdown/(?P<tournament_week>\d+)/$', signed_in_only(views.BreakdownView.as_view()), name='breakdown'),
    # /league/tournamentlist/
    url(r'^tournamentlist/$', signed_in_only(views.TournamentListView.as_view()), name='tournament_list'),
    # /league/teamcompare/
    url(r'^teamcompare/$', signed_in_only(views.TeamCompareView.as_view()), name='team_compare'),
)