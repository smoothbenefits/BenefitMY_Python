from rest_framework.views import APIView
from rest_framework.response import Response
from django.conf import settings

class EnvironmentView(APIView):
    def get(self, request, format=None):
        environment = {'env': 'NONPROD'}
        if settings.IS_PRODUCTION_ENVIRONMENT:
            environment['env'] = 'PROD'
        return Response(environment)
