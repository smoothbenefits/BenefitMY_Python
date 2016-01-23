from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from app.service.monitoring.logging_service import LoggingService

LEVELS = ['debug', 'info', 'warn', 'error']

class LoggingServiceView(APIView):

    def post(self, request, level, format=None):
        if any(level.lower() in l for l in LEVELS):
            log = LoggingService()
            print request
            data = request.DATA['data']
            if data:
                log.error(data)
            return Response(status=status.HTTP_201_CREATED)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)
