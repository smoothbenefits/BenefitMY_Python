import json
from django.http import Http404


class CorsMiddleware(object):

    def __init__(self):
        pass

    def process_response(self, request, response):
        response["Access-Control-Allow-Origin"] = "*"
        response["Access-Control-Allow-Headers"] = "Origin, X-Requested-With, Content-Type, Accept"
        response["Access-Control-Allow-Methods"] = "GET, POST, PUT, DELETE, OPTIONS"

        return response
