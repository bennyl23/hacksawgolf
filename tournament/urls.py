from django.conf.urls import patterns, url
from tournament import views
from login.functions import signed_in_only


urlpatterns = patterns('',
    # /tournament/getgolfersalary/
    # used in admin for tournaments
    url(r'^getgolfersalary/(?P<golfer_id>\d+)/$', views.getDefaultSalaryForGolfer, name='getgolfersalary'),
    # /tournament/scores/
    url(r'^scores/$', signed_in_only(views.ScoresView.as_view()), name='tournament_scores'),
    # /tournament/scores/1/
    url(r'^scores/(?P<tournament_week>\d+)/$', signed_in_only(views.ScoresView.as_view()), name='tournament_scores'),
    # /team/getteamforuserfortournament/2/6
    url(r'^getteamforuserfortournament/(?P<user_id>\d+)/(?P<tournament_id>\d+)/$', signed_in_only(views.GetTeamForUserForTournament.as_view()), name='getteamforuserfortournament'),
)