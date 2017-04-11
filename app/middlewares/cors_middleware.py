import json
from django.http import Http404


class CorsMiddleware(object):

    def __init__(self):
        pass

    def process_response(self, request, response):
        response["Access-Control-Allow-Origin"] = "*"

        return response
