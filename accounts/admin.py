from django.contrib import admin

# Register your models here.
from django.contrib.auth import get_user_model

from accounts.forms import UserCreationForm

User = get_user_model()


@admin.register(User)
class ClientAdmin(admin.ModelAdmin):
    form = UserCreationForm

    list_editable = ("is_employee",)

    list_display = (
        "sys_id",
        "name",
        "email",
        "is_employee",
        "is_staff",
        "is_superuser",
    )

    search_fields = [
        "name",
    ]
