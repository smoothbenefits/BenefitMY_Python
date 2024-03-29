from rest_framework.views import APIView
from django.http import Http404
from rest_framework.response import Response
from rest_framework import status
from django.db import transaction

from app.models.direct_deposit import DirectDeposit
from app.serializers.direct_deposit_serializer import (
    DirectDepositSerializer,
    DirectDepositPostSerializer)


class DirectDepositView(APIView):
    def _get_object(self, pk):
        try:
            return DirectDeposit.objects.get(pk=pk)
        except DirectDeposit.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        dd = DirectDeposit.objects.filter(user=pk)
        serializer = DirectDepositSerializer(dd, many=True)
        return Response(serializer.data)

    def post(self, request, pk, format=None):
        serializer = DirectDepositPostSerializer(data=request.DATA)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk, format=None):
        dd = self._get_object(pk)
        serializer = DirectDepositSerializer(dd, data=request.DATA)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        d = self._get_object(pk)
        d.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
