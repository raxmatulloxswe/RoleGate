from rest_framework import generics
from rest_framework.response import Response

from apps.common.models import AuditLog
from .serializers import CompleteRegisterSerializer


class CompleteRegisterView(generics.GenericAPIView):
    serializer_class = CompleteRegisterSerializer

    def post(self, request):
        session = request.data['session']
        if not session:
            return Response({'message': "Session Not Found"})

        serializer = self.get_serializer(data=request.data, context={'session': session})
        serializer.is_valid(raise_exception=True)
        AuditLog.objects.create(
            user=request.user,
            action="/register API",
            ip_address=self.request.META.get('REMOTE_ADDR'),
            user_agent=self.request.META.get('HTTP_USER_AGENT')
        )

        return Response({'message': "Registration Completed"})


__all__ = ['CompleteRegisterView']