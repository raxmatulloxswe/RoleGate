from django.core.cache import cache
from rest_framework import serializers

from apps.user.models import User


class CompleteRegisterSerializer(serializers.Serializer):
    session = serializers.CharField()
    opt_field = serializers.IntegerField()

    def validate(self, validated_data):
        try:
            email, password, opt, session = cache.get(f"register_{validated_data['session']}")
        except:
            raise serializers.ValidationError("Invalid Session")

        if validated_data['opt_field'] != opt or validated_data['session'] != session:
            raise serializers.ValidationError("Invalid OPT Code or Session")

        User.objects.create_user(email=email, password=password)
        cache.delete(f"register_{session}")

        return validated_data

    # def create(self, validated_data):
    #     pass