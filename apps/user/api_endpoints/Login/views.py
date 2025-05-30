from rest_framework import generics
from django.contrib.auth import authenticate
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response

from apps.common.models import AuditLog
from .serializers import LoginSerializer
from apps.user.utils import create_jwt
from ...models import RefreshToken


class LoginView(generics.GenericAPIView):
    serializer_class = LoginSerializer


    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = authenticate(
            request,
            email=serializer.validated_data['email'],
            password=serializer.validated_data['password']
        )

        if user is None:
            raise ValidationError('Email or Password Not Found')

        token = create_jwt(user.id)
        RefreshToken.objects.create(
            user=user,
            token=token['refresh']
        )
        AuditLog.objects.create(
            user=user,
            action="/login API",
            token=token['refresh'],
            ip_address=self.request.META.get('REMOTE_ADDR'),
            user_agent=self.request.META.get('HTTP_USER_AGENT')
        )
        return Response({'token': token})
