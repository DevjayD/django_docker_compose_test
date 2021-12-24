"""
    Manager for User created using AbstractBaseUser.
    UserManager is created for User to attach the objects attribute/data
"""

# python imports

# django imports
from django.contrib.auth.models import BaseUserManager


# third-party imports

# inter-app imports

# local imports


class UserManager(BaseUserManager):
    """
    Custom User Manager For User.
    """

    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError("Email Required")

        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_employee", False)
        return self._create_user(email, password, **extra_fields)
