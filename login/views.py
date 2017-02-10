from django.views.generic import FormView, RedirectView, TemplateView
from login import forms
from register.models import User
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User as DjangoUser
from django.conf import settings
from django.template.loader import get_template
from django.template import Context
from django.core.mail import EmailMultiAlternatives


class LoginView(FormView):

    form_class = forms.LoginForm
    template_name = 'login/login.html'

    # check if password needs to be reset or not and redirect appropriately
    def get_success_url(self):
        if 'user_id' in self.request.session:
            user = User.objects.get(
                user_id = self.request.session['user_id']
            )

        if 'user_id_reset_password' in self.request.session:
            user = User.objects.get(
                user_id = self.request.session['user_id_reset_password']
            )

        if user.user_reset_password:
            return reverse("login:reset_password")
        else:
            return reverse("home:home")

    # override the form_valid method to put the logged in user_id into session
    def form_valid(self, form):
        # delete session user_id variable so a user who reset their password cannot bypass the reset password flow
        if 'user_id' in self.request.session:
            del self.request.session['user_id']

        # delete the session user_id_reset_password variable
        if 'user_id_reset_password' in self.request.session:
            del self.request.session['user_id_reset_password']

        # get the validated user's user_id
        user = User.objects.get(
            user_email = form.cleaned_data.get('user_email')
        )
        if user.user_reset_password:
            # Put the user id into session but in a separate variable so the login decorator does not validate if user tries to bypass reset password flow
            self.request.session['user_id_reset_password'] = user.user_id
        else:
            # Put the user id into session
            self.request.session['user_id'] = user.user_id

        return super(LoginView, self).form_valid(form)

    def get_admin_email(self):
        return settings.EMAIL_HOST_USER


class LogoutView(RedirectView):

    pattern_name = 'login:login'

    def get_redirect_url(self, *args, **kwargs):
        # destroy the session before redirecting
        self.request.session.flush()

        return super(LogoutView, self).get_redirect_url(*args, **kwargs)


class ForgotPasswordView(FormView):

    form_class = forms.ForgotPasswordForm
    template_name = 'login/forgot_password.html'

    # override the get_success_url method to use the named url config instead of hardcoding it
    def get_success_url(self):
        return reverse("login:forgot_password_sent")

    # override the form_valid method to put the logged in user_id into session
    def form_valid(self, form):

        user = User.objects.get(user_email=form.cleaned_data['user_email'])
        user_temp_password = DjangoUser.objects.make_random_password(length=8)

        text_only_template = get_template('login/forgot_password_email.txt')
        html_template = get_template('login/forgot_password_email.html')

        # set variables to apply to the content of the email
        content = Context({'user_email':user.user_email, 'user_temp_password':user_temp_password})

        # render the email templates
        text_content = text_only_template.render(content)
        html_content = html_template.render(content)

        # set email parameters and send
        subject = 'Forgot Password'
        from_email = 'Hacksaw Golf<' + settings.EMAIL_HOST_USER + '>'
        to_emails = user.user_email
        email_msg = EmailMultiAlternatives(subject, text_content, from_email, [to_emails])
        email_msg.attach_alternative(html_content, "text/html")
        email_msg.send()

        # update the user with the new temp password and set their reset password flag
        user.user_password = user_temp_password
        user.user_password = user.hash_password()
        user.user_reset_password = True
        user.save()

        # Put the user's email into session
        self.request.session['forgot_password_user_email'] = user.user_email

        return super(ForgotPasswordView, self).form_valid(form)


class ForgotPasswordSentView(TemplateView):

    template_name = 'login/forgot_password_sent.html'

    def get_email_password_sent_to(self):
        forgot_password_user_email = self.request.session['forgot_password_user_email']
        return forgot_password_user_email


class ResetPasswordView(FormView):

    form_class = forms.ResetPasswordForm
    template_name = 'login/reset_password.html'

    # override the get_success_url method to use the named url config instead of hardcoding it
    def get_success_url(self):
        return reverse("home:home")

    # override the form_valid method hash/save the new password
    def form_valid(self, form):

        user = User.objects.get(user_id=int(self.request.session['user_id_reset_password']))

        # update the user with the new password and set their reset password flag to false
        user.user_password = form.cleaned_data['user_password']
        user.user_password = user.hash_password()
        user.user_reset_password = False
        user.save()

        # put the user_id into session
        self.request.session['user_id'] = user.user_id

        return super(ResetPasswordView, self).form_valid(form)
