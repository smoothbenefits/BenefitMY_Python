import json
import traceback
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
            record = self._map_response_for_logging(response)
            self.log.info(record)

        return response

    def process_exception(self, request, exception):
        '''
        Log exception
        '''
        self.log.error(traceback.format_exc())

        return None

    def _eligible_for_logging(self, request):
        content_type = request.META.get('CONTENT_TYPE')
        
        if not content_type:
            return False

        if not request.path.lower().startswith('/api/'):
            return False

        if (content_type.lower().find('application/json') < 0
            and content_type.lower().find('text/plain') < 0):
            return False

        return (request.method == 'PUT' or request.method == 'GET'
            or request.method == 'POST' or request.method == 'DELETE')

    def _map_request_for_logging(self, request):
        record = {
            'type': 'REQUEST',
            'path': request.path,
            'path_info': request.path_info,
            'method': request.method,
            'correlation_id': '',
            'headers': self._get_request_http_headers(request)
        }
        if hasattr(request, 'correlation_id'):
            record['correlation_id'] = request.correlation_id
        return json.dumps(record)

    def _map_response_for_logging(self, response):
        record = {
            'type': 'RESPONSE',
            'status_code': response.status_code,
            'reason_phrase': response.reason_phrase,
            'headers': self._get_response_headers(response),
            'content': response.content
        }
        return record

    def _get_response_headers(self, response):
        result = {}

        for header in response._headers:
            result[header] = response[header]

        return result

    def _get_request_http_headers(self, request):
        result = {}

        for header, value in request.META.items():
            if (header.startswith('HTTP_')
                or header == 'CONTENT_TYPE'
                or header == 'CONTENT_LENGTH'
                or header == 'QUERY_STRING'):
                result[header] = value

        return result