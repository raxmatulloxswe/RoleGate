from django.utils.crypto import get_random_string
from rest_framework import serializers
from django.core.cache import cache

from apps.user.models import User
from apps.user.utils import generate_opt


class RegisterSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField(write_only=True, min_length=8)

    class Meta:
        model = User
        fields = (
            'email',
            'password',
            'confirm_password'
        )
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')
        confirm_password = attrs.get('confirm_password')

        if password != confirm_password:
            raise serializers.ValidationError(
                "Password and Confirm Password doesn't match"
            )
        opt = generate_opt()
        session = get_random_string(length=32)
        cache.set(f"register_{session}", (email, password, opt, session), timeout=181)
        attrs['session'] = session
        return attrs
