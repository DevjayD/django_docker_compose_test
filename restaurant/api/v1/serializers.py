import csv
import io
import json
from datetime import datetime

from django.core.validators import FileExtensionValidator
from rest_framework import serializers

from accounts.messages import SYSTEM_ERROR_MESSAGE
from restaurant.models import Company, IsVoted, Menu, Restaurant, Voting


class CompanyModelSerializer(serializers.ModelSerializer):
    """
    Model Serializer for Creating the Company
    """

    class Meta:
        model = Company
        fields = (
            "id",
            "name",
            "mobile_number",
            "email",
            "last_updated",
            "timestamp",
        )

        read_only_fields = ("id", "last_updated", "timestamp")


class RestaurantModelSerializer(serializers.ModelSerializer):
    """
    Model Serializer for Creating the Company
    """

    class Meta:
        model = Restaurant
        fields = (
            "id",
            "name",
            "mobile_number",
            "email",
            "company",
            "last_updated",
            "timestamp",
        )

        read_only_fields = ("id", "last_updated", "timestamp")


class MenuModelSerializer(serializers.ModelSerializer):
    """
    Model Serializer for Menu
    """

    votes = serializers.SerializerMethodField(read_only=True)
    menu_file = serializers.FileField(
        write_only=True,
        validators=[FileExtensionValidator(allowed_extensions=["csv"])],
    )

    class Meta:
        model = Menu
        fields = (
            "id",
            "name",
            "restaurant",
            "menu",
            "menu_file",
            "votes",
            "last_updated",
            "timestamp",
        )

        read_only_fields = ("id", "last_updated", "timestamp")

    def to_representation(self, instance):
        repr = super(MenuModelSerializer, self).to_representation(instance)
        repr["menu"] = json.loads(instance.menu or '{}')
        return repr

    def get_votes(self, obj) -> int:
        votes = 0
        votes_obj = obj.menu_votes.filter(
            timestamp__date=datetime.now().date()
        ).first()
        if votes_obj:
            votes = votes_obj.votes
        return votes

    def create(self, validated_data) -> Menu:
        json_data = None
        if validated_data.get("menu_file"):
            file = (
                validated_data.pop("menu_file")
                if validated_data.get("menu_file")
                else None
            )
            decoded_file = file.read().decode("utf-8")
            io_string = io.StringIO(decoded_file)
            csv_obj = csv.reader(io_string, delimiter=";", quotechar="|")
            menu_dict = {}
            for line in csv_obj:
                menu_dict[f"{line[0].split(',')[0]}"] = line[0].split(",")[
                    1
                ]
                json_data = json.dumps(menu_dict, indent=4)
            validated_data["menu"] = json_data
        instance = super(MenuModelSerializer, self).create(validated_data)
        return instance

    def update(self, instance, validated_data) -> object:
        return super(MenuModelSerializer, self).update(
            instance, validated_data
        )


class VotingSerializer(serializers.Serializer):
    menu_id = serializers.IntegerField(
        required=True,
    )

    def validate(self, data) -> json:
        request = self.context["request"]
        menu_id = data.get("menu_id")
        menu_obj = Menu.objects.get(id=menu_id)
        if not menu_obj:
            raise serializers.ValidationError(
                SYSTEM_ERROR_MESSAGE["ENTER_A_VALID_MENU_ID"]
            )
        else:
            is_voted = IsVoted.objects.filter(
                user=request.user, timestamp__date=datetime.now().date()
            )
            if is_voted:
                raise serializers.ValidationError(
                    SYSTEM_ERROR_MESSAGE["ALREADY_VOTED"]
                )
            else:
                voting_obj, created = Voting.objects.get_or_create(
                    menu_id=menu_id
                )
                IsVoted.objects.create(user=request.user)
                voting_obj.votes += 1
                voting_obj.save()
        return data
