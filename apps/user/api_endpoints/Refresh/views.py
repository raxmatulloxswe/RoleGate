from django.core.cache import cache
from rest_framework import generics
from rest_framework.response import Response

from .serializers import RefreshSerializer
from apps.user.utils import create_jwt
from ...models import RefreshToken
from apps.common.models import AuditLog


class RefreshView(generics.GenericAPIView):
    serializer_class = RefreshSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user  = serializer.context['user']
        jwt_token= create_jwt(user.id)

        old_refresh = serializer.context['token']
        print("\n[OLD REFRESH]", old_refresh)
        print("[NEW REFRESH]", jwt_token['refresh'])
        save = RefreshToken.objects.filter(token=old_refresh).delete()
        print('\n[DELETE]', save)

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
