from datetime import datetime

from rest_framework import serializers

from accounts.messages import SYSTEM_ERROR_MESSAGE
from restaurant.models import IsVoted, Menu, Voting


class VotingSerializer(serializers.Serializer):
    menu_id = serializers.ListField(
        required=True,
    )

    def validate(self, data) -> list:
        request = self.context["request"]
        menu_id = data.get("menu_id")
        for id in menu_id:
            menu_obj = Menu.objects.filter(id=id)
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
                weight = 3
                for id in menu_id:
                    voting_obj, created = Voting.objects.get_or_create(
                        menu_id=id
                    )
                    voting_obj.votes += weight
                    weight -= 1
                    voting_obj.save()
                IsVoted.objects.create(user=request.user)
        return data
