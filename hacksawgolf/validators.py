from django.core.validators import ValidationError


class BaseValidator(object):

    def __init__(self):
        self.validation_error = ''
        self.is_valid = True
