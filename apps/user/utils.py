from datetime import datetime, timedelta

import jwt
from django.conf import settings
from django.core.cache import cache


def create_jwt(user_id):
    now = datetime.now()
    exp = now + timedelta(minutes=15)
    refresh_exp = now + timedelta(days=7)

    access_payload = {
        'user_id': user_id,
        'type': 'access',
        'iat': int(now.timestamp()),
        'exp': int(exp.timestamp())
    }
    refresh_payload = {
        'user_id': user_id,
        'type': 'refresh',
        'iat': int(now.timestamp()),
        'exp': int(refresh_exp.timestamp())
    }

    eccess_token = jwt.encode(
        access_payload, settings.SECRET_KEY, algorithm='HS256'
    )
    refresh_token = jwt.encode(
        refresh_payload, settings.SECRET_KEY, algorithm='HS256'
    )
    if isinstance(eccess_token, bytes):
        eccess_token = eccess_token.decode('utf-8')

    cache.set(eccess_token, "access_token_valid", timeout=15 * 60)

    return {
        'access': eccess_token,
        'refresh': refresh_token
    }

def generate_opt():
    import random
    return random.randint(1000, 9999)
