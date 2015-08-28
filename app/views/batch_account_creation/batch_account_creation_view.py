import json
from django.http import Http404
from django.db import transaction
from rest_framework.views import APIView
from rest_framework.response import Response


class BatchAccountCreationView(APIView):

    @transaction.atomic
    def post(self, request, company_id, format=None):
        items = json.loads(request.DATA)

        for item in items:
            print item

        return Response({'result': items})
