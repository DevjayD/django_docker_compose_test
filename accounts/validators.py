from django.core.validators import RegexValidator

from accounts.messages import VALIDATION_ERROR_MESSAGES

NameValidator = RegexValidator(
    regex="^[a-zA-Z.\s]{2,150}$",
    message=VALIDATION_ERROR_MESSAGES["INVALID_NAME"],
    code="INVALID_NAME",
)
