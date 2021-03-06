from django.conf.urls import patterns, url
from home import views
from login.functions import signed_in_only


urlpatterns = patterns('',
    # / or /home/
    url(r'^$', signed_in_only(views.HomeView.as_view()), name='home'),
    # /home/3/
    url(r'^(?P<tournament_week>\d+)/$', signed_in_only(views.HomeView.as_view()), name='home'),
)