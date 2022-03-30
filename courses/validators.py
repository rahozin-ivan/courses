from django.core.exceptions import ValidationError

from datetime import date


def validate_date(value):
    if value < date.today():
        raise ValidationError(f"{value} is not correct! Specify date that's not in the past!")
