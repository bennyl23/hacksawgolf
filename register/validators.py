from register.models import User
from hacksawgolf.validators import BaseValidator
from django.core.exceptions import ValidationError


# register form inline validators
def validate_user_email(value):
    existing_user_email = User.objects.filter(user_email=value)
    if len(existing_user_email):
        raise ValidationError('This email address has an existing account associated with it.  Try another.')

def validate_user_team_name(value):
    existing_team_name = User.objects.filter(user_team_name=value)
    if len(existing_team_name):
        raise ValidationError('This team name is being used by another player.  Try another.')

def validate_referring_email(value):
    existing_referring_email = User.objects.filter(user_email=value)
    if (not existing_referring_email):
        raise ValidationError('This email could not be found.  Try again.')


# register validator class (used to validate anything that can't be handled by inline form validators)
class RegisterValidator(BaseValidator):

    def __init__(self, user_to_validate, user_password_again):
        super(RegisterValidator, self).__init__()
        self.user_to_validate = user_to_validate
        self.user_password_again = user_password_again

    def validate_passwords_match(self):
        if self.user_to_validate.user_password != self.user_password_again:
            self.is_valid = False
            self.validation_error = 'The passwords you entered do not match.  Please enter the same password twice.'
