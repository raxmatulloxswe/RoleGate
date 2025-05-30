from rest_framework import generics, permissions
from rest_framework.response import Response

from apps.common.models import AuditLog
from .serializers import LogOutSerializer
from apps.user.models import RefreshToken, BlackListedToken


class LogOutView(generics.GenericAPIView):
    serializer_class = LogOutSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        refresh = serializer.validated_data['refresh']
        access = serializer.validated_data['access']
        user = request.user
        user_agent = self.request.META.get('HTTP_USER_AGENT')

        RefreshToken.objects.filter(
            user=user, token=refresh
        ).delete()
        BlackListedToken.objects.create(
            user=user,
            token=access,
            token_type=BlackListedToken.TOKEN_TYPE_CHOICES.ACCESS,
            action="/logout API",
            user_agent=user_agent
        )
        BlackListedToken.objects.create(
            user=user,
            token=refresh,
            token_type=BlackListedToken.TOKEN_TYPE_CHOICES.REFRESH,
            action="/logout API",
            user_agent=user_agent
        )
        AuditLog.objects.create(
            user=user,
            action="/logout API",
            ip_address=self.request.META.get('REMOTE_ADDR'),
            user_agent=user_agent
        )

        return Response({'message': "Logout Success"})
