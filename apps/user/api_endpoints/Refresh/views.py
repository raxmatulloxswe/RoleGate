from django.core.cache import cache
from rest_framework import generics
from rest_framework.response import Response

from .serializers import RefreshSerializer
from apps.user.utils import create_jwt
from ...models import RefreshToken, BlackListedToken
from apps.common.models import AuditLog
from ...throttle import CustomRateThrottle


class RefreshView(generics.GenericAPIView):
    serializer_class = RefreshSerializer
    throttle_classes = (CustomRateThrottle,)

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user  = serializer.context['user']
        jwt_token= create_jwt(user.id)

        old_refresh = serializer.context['token']
        old_access = request.META.get('HTTP_AUTHORIZATION', '').split('Bearer ')[-1]
        RefreshToken.objects.filter(token=old_refresh).delete()
        if old_access:
            BlackListedToken.objects.create(
                user=user,
                token=old_access,
                token_type=BlackListedToken.TOKEN_TYPE_CHOICES.ACCESS,
                action="/refresh API",
                user_agent=self.request.META.get('HTTP_USER_AGENT')
            )
        BlackListedToken.objects.create(
            user=user,
            token=old_refresh,
            token_type=BlackListedToken.TOKEN_TYPE_CHOICES.REFRESH,
            action="/refresh API",
            user_agent=self.request.META.get('HTTP_USER_AGENT')
        )
        RefreshToken.objects.create(
            user=user,
            token=jwt_token['refresh']
        )
        AuditLog.objects.create(
            user=user,
            action="/refresh API",
            token=jwt_token['refresh'],
            ip_address=self.request.META.get('REMOTE_ADDR'),
            user_agent=self.request.META.get('HTTP_USER_AGENT')
        )

        return Response({
            'access': jwt_token['access'],
            'refresh': jwt_token['refresh'],
        })
