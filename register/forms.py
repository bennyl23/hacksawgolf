from django import forms
from register import validators
from register.models import User


class RegisterForm(forms.ModelForm):

    user_email = forms.EmailField(
        max_length=50,
        label='Email',
        initial='',
        widget=forms.TextInput(
            attrs={'placeholder':'Enter email', 'class':'form-control', 'autofocus':'autofocus'}
        ),
        validators=[validators.validate_user_email]
    )
    user_password = forms.CharField(
        min_length=8,
        max_length=60,
        label='Password',
        initial='',
        widget=forms.PasswordInput(
            attrs={'placeholder':'Enter password', 'class':'form-control'}
        ),
        error_messages={'min_length':'Password must be at least 8 characters.'}
    )
    user_password_again = forms.CharField(
        min_length=8,
        max_length=60,
        label='Re-enter Password',
        initial='',
        widget=forms.PasswordInput(
            attrs={'placeholder':'Re-enter password', 'class':'form-control'}
        ),
        error_messages={'min_length':'Password must be at least 8 characters.'}
    )
    user_team_name = forms.CharField(
        min_length=5,
        max_length=20,
        label='Team name (20 char max)',
        initial='',
        widget=forms.TextInput(
            attrs={'placeholder':'Enter team name', 'class':'form-control'}
        ),
        validators=[validators.validate_user_team_name],
        error_messages={'min_length':'Team name must be at least 5 characters.'}
    )
    user_referring_email = forms.EmailField(
        max_length=50,
        label='Referring email',
        initial='',
        widget=forms.TextInput(
            attrs={'placeholder':'Enter referring email', 'class':'form-control'}
        ),
        validators=[validators.validate_referring_email]
    )

    # Model form classes will create inputs for all model fields not implicitly declared unless told otherwise
    class Meta:
        model = User
        exclude = ['user_af1', 'user_af2', 'user_real_name', 'user_paid', 'message_from_commish']

    # override the form's clean method to validate the registration information against the db
    def clean(self):
        cleaned_data = super(RegisterForm, self).clean()

        # check for other form errors (field validation) before validating the two passwords
        if not self.errors:
            user_to_validate = User(
                                    user_email = cleaned_data['user_email'],
                                    user_password = cleaned_data['user_password'],
                                    user_referring_email = cleaned_data['user_referring_email'],
                                    user_team_name = cleaned_data['user_team_name']
                                    )
            register_validator = validators.RegisterValidator(user_to_validate, cleaned_data['user_password_again'])
            register_validator.validate_passwords_match()

            # if passwords do not match, raise an error
            if not register_validator.is_valid:
                # Send back an error
                raise forms.ValidationError(register_validator.validation_error)

        return cleaned_data
