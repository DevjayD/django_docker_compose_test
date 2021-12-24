from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.utils.translation import gettext_lazy as _

# Third Party Import
from phonenumber_field.modelfields import PhoneNumberField

# InterApp Imports
from accounts.managers import UserManager
from accounts.messages import HELP_TEXTS
from accounts.validators import NameValidator


class User(AbstractBaseUser, PermissionsMixin):
    name = models.CharField(
        _("name"),
        max_length=150,
        validators=[
            NameValidator,
        ],
    )

    mobile_number = PhoneNumberField(
        _("mobile number"), unique=True, blank=True, null=True
    )

    email = models.EmailField(_("email address"), unique=True)

    is_staff = models.BooleanField(
        _("staff status"), default=False, help_text=HELP_TEXTS["IS_STAFF"]
    )

    is_employee = models.BooleanField(
        _("employee status"),
        default=True,
        help_text=HELP_TEXTS["IS_STAFF"],
    )

    is_active = models.BooleanField(
        _("active"), default=True, help_text=HELP_TEXTS["IS_ACTIVE"]
    )

    date_joined = models.DateTimeField(_("date joined"), auto_now_add=True)

    objects = UserManager()

    EMAIL_FIELD = "email"
    USERNAME_FIELD = "email"

    class Meta:
        ordering = [
            "-id",
        ]
        verbose_name = _("user")
        verbose_name_plural = _("users")

    def __str__(self):
        return self.sys_id

    @property
    def sys_id(self):
        return "USR{}".format(str(self.id).zfill(6))
