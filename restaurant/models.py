from django.contrib.auth import get_user_model
from django.db import models
from django.db.models import JSONField
from django.utils.translation import gettext_lazy as _

from utils.abstaract_models import (
    AbstractTimeStampModel,
    AbstractMobileEmailModel,
)

# Third Party Import

# InterApp Imports
User = get_user_model()


class Company(AbstractTimeStampModel, AbstractMobileEmailModel):
    name = models.CharField(max_length=100, unique=True)

    class Meta:
        ordering = [
            "-id",
        ]
        verbose_name = _("Company")
        verbose_name_plural = _("Company")

    @property
    def sys_id(self):
        return "COMPANY-{}".format(str(self.id).zfill(6))

    def __str__(self):
        return f"COMPANY-{self.id} | {self.name}"


class Restaurant(AbstractTimeStampModel, AbstractMobileEmailModel):
    name = models.CharField(max_length=100, unique=True)
    company = models.ForeignKey(
        Company,
        on_delete=models.CASCADE,
        related_name="company",
        verbose_name=_("Company"),
    )

    class Meta:
        ordering = [
            "-id",
        ]
        verbose_name = _("Restaurant")
        verbose_name_plural = _("Restaurant")

    def __str__(self):
        return f"RESTAURANT-{self.id} | {self.name}"

    @property
    def sys_id(self):
        return "RESTAURANT-{}".format(str(self.id).zfill(6))


class Menu(AbstractTimeStampModel):
    name = models.CharField(max_length=100)
    restaurant = models.ForeignKey(
        Restaurant,
        on_delete=models.CASCADE,
        related_name="restaurant_menu",
        verbose_name=_("Restaurant Menu"),
    )
    menu = JSONField(_("menu"), blank=True, null=True)

    class Meta:
        ordering = [
            "-timestamp",
        ]
        verbose_name = _("Menu")
        verbose_name_plural = _("Menu")

    @property
    def sys_id(self):
        return "MENU-{}".format(str(self.id).zfill(6))


class Voting(AbstractTimeStampModel):
    menu = models.ForeignKey(
        Menu,
        on_delete=models.CASCADE,
        related_name="menu_votes",
        verbose_name=_("Total Votes"),
    )
    votes = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = [
            "-votes",
        ]
        verbose_name = _("Voting")
        verbose_name_plural = _("Voting")

    def __str__(self):
        return f"Voting For {self.menu.name}"

    @property
    def sys_id(self):
        return "VOTES-{}".format(str(self.id).zfill(6))


class IsVoted(AbstractTimeStampModel):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="user_voted",
        verbose_name=_("User Voted"),
    )
