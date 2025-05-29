from datetime import datetime, timedelta

import jwt
from django.conf import settings


def create_jwt(user_id):
    now = datetime.now()
    exp = now + timedelta(seconds=180)
    refresh_exp = now + timedelta(days=7)

    access_payload = {
        'user_id': user_id,
        'iat': int(now.timestamp()),
        'exp': int(exp.timestamp())
    }
    refresh_payload = {
        'user_id': user_id,
        'iat': int(now.timestamp()),
        'exp': int(refresh_exp.timestamp())
    }

    eccess_token = jwt.encode(
        access_payload, settings.SECRET_KEY, algorithm='HS256'
    )
    refresh_token = jwt.encode(
        refresh_payload, settings.SECRET_KEY, algorithm='HS256'
    )

    return {
        'access': eccess_token,
        'refresh': refresh_token
    }

def generate_opt():
    import random
    return random.randint(1000, 9999)
