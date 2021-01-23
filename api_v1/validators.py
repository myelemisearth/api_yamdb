from datetime import datetime
from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator, MinValueValidator

RANGE_ERROR_MESSAGE = 'Entered value must be between 1 and 10'


def custom_year_validator(value):
    if value > datetime.now().year:
        raise ValidationError(
            ('Year cant be greater then current.'),
            params={'value': value},
        )
