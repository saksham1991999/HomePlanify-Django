from rest_framework import serializers
from rest_framework.fields import CurrentUserDefault
from datetime import datetime

from .models import Firm, Zone


class ZoneSerializer(serializers.ModelSerializer):

    class Meta:
        model = Zone
        fields = (
            "id",
            "name",
            "areas",
        )


class FirmSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )

    class Meta:
        model = Firm
        fields = (
            "id",
            "user",
            "name",
            "email",
            "firm_name",
            "zone",
            "deals",
            "office_address",
            "home_address",
            "phone",
            "bloodgroup",
        )
