from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import permissions

from apps.common.permissions import IsManager, IsAdmin, IsUser


class hello(APIView):
    permission_classes = [IsUser]

    def get(self, request, format=None):
        content = {
            'status': 'Success',
        }
        return Response(content)


class StatisticsForManagerApiView(APIView):
    permission_classes = [IsManager]

    def get(self, request):
        content = {
            'status': 'Blah Blah Statistics',
        }
        return Response(content)


class StatisticsForAdminApiView(APIView):
    permission_classes = [IsAdmin]

    def get(self, request):
        content = {
            'status': "Hayot go'zal",
        }
        return Response(content)
