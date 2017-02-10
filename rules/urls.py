from django.conf.urls import patterns, url
from rules import views
from login.functions import signed_in_only


urlpatterns = patterns('',
    # /rules/
    url(r'^$', signed_in_only(views.RuleView.as_view()), name='rules')
)