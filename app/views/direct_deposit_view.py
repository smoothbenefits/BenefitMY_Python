from rest_framework.views import APIView
from django.http import Http404
from rest_framework.response import Response
from rest_framework import status
from django.db import transaction

from app.models.direct_deposit import DirectDeposit
from app.serializers.direct_deposit_serializer import DirectDepositSerializer


class DirectDepositView(APIView):
    def _get_object(self, pk):
        try:
            return DirectDeposit.objects.get(user=pk)
        except DirectDeposit.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        dd = self._get_object(pk)
        serializer = DirectDepositSerializer(dd)
        return Response(serializer.data)
