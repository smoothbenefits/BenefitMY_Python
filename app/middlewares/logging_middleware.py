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
            # remove request body for security reasons
            record = self._map_request_for_logging(request)
            self.log.info(record)

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

    def _map_request_for_logging(self, request):
        record = {
            'path': request.path,
            'path_info': request.path_info,
            'method': request.method,
            'query_string': request.META['QUERY_STRING'],
            'correlation_id': ''
        }
        if hasattr(request, 'correlation_id'):
            record['correlation_id'] = request.correlation_id
        return json.dumps(record)
