from rest_framework.exceptions import ValidationError

from BookSelling.settings import TEL_NUMBER_LENGHT_MIN, TEL_NUMBER_LENGHT_MAX


def validate_phone_number(value):
    """Phone number validator."""
    if not (value.isdigit() or value[0] == '+' and value[1:].isdigit()):
        raise ValidationError("Phone number should not contain letters")

    if len(value) > TEL_NUMBER_LENGHT_MAX or len(value) < TEL_NUMBER_LENGHT_MIN:
        raise ValidationError(
            "Phone number should not have more than {} digits or less than {}".format(TEL_NUMBER_LENGHT_MAX,
                                                                                      TEL_NUMBER_LENGHT_MIN))
