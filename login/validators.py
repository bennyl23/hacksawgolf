from hacksawgolf.validators import BaseValidator
from django.contrib.auth.hashers import check_password
from register.models import User


class LoginValidator(BaseValidator):

    def __init__(self, user_to_validate):
        super(LoginValidator, self).__init__()
        self.user_to_validate = user_to_validate

    def validate_user(self):
        try:
            user = User.objects.get(
                user_email=self.user_to_validate.user_email
            )
        except User.DoesNotExist:
            self.is_valid = False
            self.validation_error = 'The email you entered is not in the system.  Please try again.'
        except User.MultipleObjectsReturned:
            self.is_valid = False
            self.validation_error = 'There are multiple accounts that use the email you entered.  Please contact the commish.'
        except:
            self.is_valid = False
            self.validation_error = 'There was an error during the sign in process.  Please try again.'
        else:
            # check the plain text password against the hash in the database
            if not check_password(self.user_to_validate.user_password, user.user_password):
                self.is_valid = False
                self.validation_error = 'The password you entered is incorrect.  Please try again.'


class ForgotPasswordValidator(BaseValidator):

    def __init__(self, user_to_validate):
        super(ForgotPasswordValidator, self).__init__()
        self.user_to_validate = user_to_validate

    def validate_user(self):
        try:
            user = User.objects.get(
                user_email=self.user_to_validate.user_email
            )
        except User.DoesNotExist:
            self.is_valid = False
            self.validation_error = 'The email you entered is not in the system.  Please try again.'


class ResetPasswordValidator(BaseValidator):

    def __init__(self, user_password, user_password_again):
        super(ResetPasswordValidator, self).__init__()
        self.user_password = user_password
        self.user_password_again = user_password_again

    def validate_passwords_match(self):
        if self.user_password != self.user_password_again:
            self.is_valid = False
            self.validation_error = 'The passwords you entered do not match.  Please enter the same password twice.'
