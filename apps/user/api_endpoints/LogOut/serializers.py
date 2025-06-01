import jwt
from rest_framework import serializers
from django.conf import settings

from apps.user.models import RefreshToken, BlackListedToken


class LogOutSerializer(serializers.Serializer):
    refresh = serializers.CharField()
    access = serializers.CharField()

    def validate(self, data):
        tokens = [data['refresh'], data['access']]
        for token in tokens:
            try:
                jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
            except jwt.ExpiredSignatureError:
                pass  # still add to blacklist
            except jwt.DecodeError:
                raise serializers.ValidationError("Invalid token")

        return data
