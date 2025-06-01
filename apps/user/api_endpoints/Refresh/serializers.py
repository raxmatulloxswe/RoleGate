from django.conf import settings
from rest_framework import serializers
import jwt

from apps.user.models import RefreshToken, User


class RefreshSerializer(serializers.Serializer):
    refresh = serializers.CharField()

    def validate_refresh(self, value):
        try:
            token = jwt.decode(value, settings.SECRET_KEY, algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise serializers.ValidationError('Token has expired')
        except jwt.DecodeError:
            raise serializers.ValidationError('Token is invalid')

        if token.get('type') != 'refresh':
            raise serializers.ValidationError('Invalid token type')

        if not RefreshToken.objects.filter(token=value).exists():
            raise serializers.ValidationError('Token does not exist')

        try:
            user = User.objects.get(id=token.get('user_id'))
        except User.DoesNotExist:
            raise serializers.ValidationError('User does not exist')

        self.context['user'] = user
        self.context['token'] = value
        return value
