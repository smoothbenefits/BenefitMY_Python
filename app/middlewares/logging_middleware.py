import json
from app.service.monitoring.logging_service import LoggingService
from django.http import Http404


class LoggingMiddleware(object):

    def __init__(self):
        self.log = LoggingService()

    def process_request(self, request):
        '''
        Log JSON requests
        '''
        if (self._eligible_for_logging(request)):
            self.log.info(request)

        return None

    def process_response(self, request, response):
        '''
        Log response of JSON requests
        '''
        if (self._eligible_for_logging(request)):
            self.log.info(response)

        return response

    def process_exception(self, request, exception):
        '''
        Log exception
        '''
        self.log.error(exception)

        return None

    def _eligible_for_logging(self, request):
        if not request.META.get('CONTENT_TYPE'):
            return False

        if request.META.get('CONTENT_TYPE').find('application/json') < 0:
            return False

        return (request.method == 'PUT' or request.method == 'GET'
            or request.method == 'POST' or request.method == 'DELETE')
