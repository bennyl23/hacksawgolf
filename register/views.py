from django.views.generic import CreateView
from register import forms
from register.models import User
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from tournament.models import Tournament
from django.utils import timezone


class RegisterView(CreateView):
    model = User
    form_class = forms.RegisterForm
    template_name = 'register/register.html'

    # see if the first tournament has started
    def has_first_tournament_started(self):
        try:
            tournament = Tournament.objects.get(tournament_week=1)
        except Tournament.DoesNotExist:
            return False

        if tournament.picks_lock_date <= timezone.now():
            return True
        else:
            return False

    # override the get_success_url method to use the named url config instead of hardcoding it
    def get_success_url(self):
        return reverse("home:home")

    # override the form_valid method (which would normally saves the model to the db) so the password can be hashed before saving
    def form_valid(self, form):
        user_new = User(
                       user_email = form.cleaned_data['user_email'],
                       user_team_name = form.cleaned_data['user_team_name'],
                       user_referring_email = form.cleaned_data['user_referring_email'],
                       user_password = form.cleaned_data['user_password']
                       )
        # hash the plain text password
        user_new.user_password = user_new.hash_password()
        # save the new user
        user_new.save()
        # Put the user id into session
        self.request.session['user_id'] = user_new.user_id
        # send the user to the success url
        return HttpResponseRedirect(self.get_success_url())