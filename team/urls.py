from django.conf.urls import patterns, url
from team import views
from login.functions import signed_in_only


urlpatterns = patterns('',
    # /team/
    url(r'^$', signed_in_only(views.TeamView.as_view()), name='team'),
    # /team/edit/
    url(r'^edit/$', signed_in_only(views.TeamView.as_view()), name='edit_team'),
    # /team/1/
    url(r'^(?P<tournament_week>\d+)/$', signed_in_only(views.TeamView.as_view()), name='team'),
    # /team/getgolferfortournament/5/33/2
    url(r'^getgolferfortournament/(?P<tournament_id>\d+)/(?P<golfer_id>\d+)/(?P<counter>\d+)/$', signed_in_only(views.GetGolferForTournament.as_view()), name='getgolferfortournament'),
    # /team/validateteamselect/
    url(r'^validateteamselect/$', signed_in_only(views.ValidateTeamSelect.as_view()), name='validateteamselect'),
    # /team/verify/
    url(r'^verify/$', signed_in_only(views.VerifyTeamView.as_view()), name='verify_team'),
    # /team/save/
    url(r'^save/$', signed_in_only(views.SaveTeamView.as_view()), name='save_team'),
)