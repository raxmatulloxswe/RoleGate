from django.core.cache import cache
from django.core.mail import EmailMessage
from rest_framework import generics
from rest_framework.response import Response

from .serializers import RegisterSerializer
from ...throttle import CustomRateThrottle


class SendOTPView(generics.GenericAPIView):
    serializer_class = RegisterSerializer
    throttle_classes = (CustomRateThrottle)

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data['email']
        session = serializer.validated_data['session']

        get_otp = cache.get(f"register_{session}")[2]
        subject = "Your OTP Code for Registration RoleGate API"
        message = f"Your OTP Code is {get_otp}"
        email_msg = EmailMessage(subject, message, to=[email])
        email_msg.send()

        return Response({'message': "OTP has been sent to your email!", 'session': session})


__all__ = [
    'SendOTPView'
]
