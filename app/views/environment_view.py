from rest_framework.views import APIView
from rest_framework.response import Response
from django.conf import settings

class EnvironmentView(APIView):
    def get(self, request, format=None):
        environment = {'env': settings.ENVIRONMENT}
        return Response(environment)


class TimeTrackingAppView(APIView):
    def get(self, request, format=None):
        hostname = {'hostname': settings.TIMETRACKINGAPPHOSTNAME}
        return Response(hostname)
