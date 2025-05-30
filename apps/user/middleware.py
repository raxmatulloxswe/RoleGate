import jwt
from django.conf import settings
from django.http import JsonResponse

from .models import BlackListedToken

class JWTBlackLIstMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        auth_header = request.META.get('HTTP_AUTHORIZATION', '')
        if auth_header.startswith('Bearer '):
            token = auth_header.split(' ')[1]

            if BlackListedToken.objects.filter(token=token).exists():
                return JsonResponse({"detail": "Token is blacklisted"}, status=401)

            try:
                payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
                request.user_id = payload.get('user_id')
            except jwt.ExpiredSignatureError:
                return JsonResponse({"detail": "Token has expired"}, status=401)
            except jwt.DecodeError:
                return JsonResponse({"detail": "Token is invalid"}, status=401)

        response = self.get_response(request)
        return response
