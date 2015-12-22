from rest_framework.views import APIView
from rest_framework.response import Response
from django.conf import settings

class EnvironmentView(APIView):
    def get(self, request, format=None):
        if settings.IS_PRODUCTION_ENVIRONMENT:
            return Response("PROD")
        else:
            return Response("NONPROD")
