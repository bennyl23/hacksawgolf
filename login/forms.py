from django import forms
from register.models import User
from login.validators import LoginValidator, ForgotPasswordValidator, ResetPasswordValidator


class LoginForm(forms.Form):
    user_email = forms.EmailField(
        max_length=60,
        label='Email',
        initial='',
        widget=forms.TextInput(
            attrs={'placeholder':'Enter email', 'class':'form-control', 'autofocus':'autofocus'}
        )
    )
    user_password = forms.CharField(
        max_length=60,
        label='Password',
        initial='',
        widget=forms.PasswordInput(
            attrs={'placeholder':'Enter password', 'class':'form-control'}
        )
    )

    # override the form's clean method to validate the login information
    def clean(self):
        cleaned_data = super(LoginForm, self).clean()

        # check for other form errors (field validation) before validating the username/password against the db
        if not self.errors:
            user_to_validate = User(
                                    user_email = cleaned_data['user_email'],
                                    user_password = cleaned_data['user_password'],
                                    )
            login_validator = LoginValidator(user_to_validate)
            login_validator.validate_user()

            # if login info somehow invalid, raise a validation error
            if not login_validator.is_valid:
                # Send back an error
                raise forms.ValidationError(login_validator.validation_error)

        return cleaned_data


class ForgotPasswordForm(forms.Form):
    user_email = forms.EmailField(
        max_length=60,
        label='Email',
        initial='',
        widget=forms.TextInput(
            attrs={'placeholder':'Enter email', 'class':'form-control', 'autofocus':'autofocus'}
        )
    )

    # override the form's clean method to validate the user email
    def clean(self):
        cleaned_data = super(ForgotPasswordForm, self).clean()

        # check for other form errors (field validation) before validating the user email against the db
        if not self.errors:
            user_to_validate = User(
                                    user_email = cleaned_data['user_email']
                                    )
            forgot_password_validator = ForgotPasswordValidator(user_to_validate)
            forgot_password_validator.validate_user()

            # if login info somehow invalid, raise a validation error
            if not forgot_password_validator.is_valid:
                # Send back an error
                raise forms.ValidationError(forgot_password_validator.validation_error)

        return cleaned_data


class ResetPasswordForm(forms.Form):
    user_password = forms.CharField(
        max_length=60,
        label='New password',
        initial='',
        widget=forms.PasswordInput(
            attrs={'placeholder':'Enter new password', 'class':'form-control', 'autofocus':'autofocus'}
        )
    )
    user_password_again = forms.CharField(
        max_length=60,
        label='Re-enter password',
        initial='',
        widget=forms.PasswordInput(
            attrs={'placeholder':'Re-enter password', 'class':'form-control'}
        )
    )

    # override the form's clean method to check if the passwords match
    def clean(self):
        cleaned_data = super(ResetPasswordForm, self).clean()

        # check for other form errors (field validation) before validating the two passwords
        if not self.errors:
            reset_password_validator = ResetPasswordValidator(
                                                              cleaned_data['user_password'],
                                                              cleaned_data['user_password_again']
                                                              )
            reset_password_validator.validate_passwords_match()

            # if passwords do not match, raise an error
            if not reset_password_validator.is_valid:
                # Send back an error
                raise forms.ValidationError(reset_password_validator.validation_error)

        return cleaned_data