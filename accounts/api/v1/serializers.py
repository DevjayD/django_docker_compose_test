import json

from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from rest_framework import serializers

from accounts.messages import VALIDATION_ERROR_MESSAGES

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ("id", "name", "email", "password")
        read_only_fields = ("id", "is_employee", "is_staff")

    def create(self, validated_data) -> object:
        password = (
            validated_data.pop("password")
            if validated_data.get("password")
            else None
        )
        instance = super(UserSerializer, self).create(validated_data)
        instance.set_password(password)
        instance.save()
        return instance


class UserLoginSerializer(serializers.Serializer):
    email = serializers.CharField(required=True)
    password = serializers.CharField(required=True)

    def validate(self, data) -> json:
        email = data.get("email", None)
        password = data.get("password", None)
        if not email and not password:
            raise ValidationError(
                VALIDATION_ERROR_MESSAGES["DETAILS_NOT_ENTERED"]
            )
        user = User.objects.filter(email=email)
        if not user.exists():
            raise ValidationError(
                VALIDATION_ERROR_MESSAGES["NO_USER_EXISTS"]
            )
        return data
