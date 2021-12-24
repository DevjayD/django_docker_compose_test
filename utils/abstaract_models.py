from django.db import models
from django.utils.translation import gettext_lazy as _
from phonenumber_field.modelfields import PhoneNumberField


class AbstractTimeStampModel(models.Model):
    last_updated = models.DateTimeField(
        _("Updated on"),
        auto_now=True,
    )

    timestamp = models.DateTimeField(
        _("Created on"),
        auto_now_add=True,
    )

    class Meta:
        abstract = True


class AbstractMobileEmailModel(models.Model):
    mobile_number = PhoneNumberField(_("Mobile Number"))
    email = models.EmailField(_("Email Address"), blank=True, null=True)

    class Meta:
        abstract = True
