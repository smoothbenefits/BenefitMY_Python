import json
from django.http import Http404
from django.db import transaction
from rest_framework.views import APIView
from rest_framework.response import Response


class AccountInfoListParseView(APIView):
    def post(self, request, company_id, format=None):
        rawData = request.DATA
        return Response(rawData)
