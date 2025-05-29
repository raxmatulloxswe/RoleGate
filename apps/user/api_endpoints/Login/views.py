from rest_framework import generics
from django.contrib.auth import authenticate
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response

from .serializers import LoginSerializer
from apps.user.utils import create_jwt


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
        return Response({'token': token})
