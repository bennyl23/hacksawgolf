from django.conf.urls import patterns, url
from login import views


urlpatterns = patterns('',
    # /login/
    url(r'^$', views.LoginView.as_view(), name='login'),
    # /login/logout/
    url(r'^logout/$', views.LogoutView.as_view(), name='logout'),
    # /login/forgotpassword/
    url(r'^forgotpassword/$', views.ForgotPasswordView.as_view(), name='forgot_password'),
    # /login/forgotpasswordsent/
    url(r'^forgotpasswordsent/$', views.ForgotPasswordSentView.as_view(), name='forgot_password_sent'),
    # /login/forgotpasswordsent/
    url(r'^resetpassword/$', views.ResetPasswordView.as_view(), name='reset_password'),
)