from django.conf.urls import patterns, url
from register import views


urlpatterns = patterns('',
    # /register/
    url(r'^$', views.RegisterView.as_view(), name='register')
)