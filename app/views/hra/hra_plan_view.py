from django.db import transaction
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from app.models.hra.hra_plan import HraPlan
from app.serializers.hra.hra_plan_serializer import (
    HraPlanSerializer)

class HraPlanView(APIView):
    def _get_object(self, pk):
        try:
            return HraPlan.objects.get(pk=pk)
        except HraPlan.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        plans = self._get_object(pk)
        serializer = HraPlanSerializer(plans)
        return Response(serializer.data)

    @transaction.atomic
    def delete(self, request, pk, format=None):
        plan = self._get_object(pk)
        plan.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @transaction.atomic
    def put(self, request, pk, format=None):
        plan = self._get_object(pk)
        serializer = HraPlanSerializer(plan, data=request.DATA)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @transaction.atomic
    def post(self, request, pk, format=None):
        serializer = HraPlanSerializer(data=request.DATA)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
