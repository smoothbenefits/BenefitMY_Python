from rest_framework.views import APIView
from django.http import Http404

from rest_framework import status
from rest_framework.response import Response

from app.models.company_user import CompanyUser
from app.models.fsa.fsa_plan import FsaPlan
from app.serializers.fsa.fsa_plan_serializer import (
    FsaPlanSerializer, 
    FsaPlanPostSerializer)


class FsaPlanView(APIView):
    def _get_object(self, pk):
        try:
            return FsaPlan.objects.get(pk=pk)
        except FsaPlan.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        plans = self._get_object(pk)
        serializer = FsaPlanSerializer(plans)
        return Response(serializer.data)

    def delete(self, request, pk, format=None):
        plan = self._get_object(pk)
        plan.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def put(self, request, pk, format=None):
        plan = self._get_object(pk)
        serializer = FsaPlanPostSerializer(plan, data=request.DATA)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def post(self, request, pk, format=None):
        serializer = FsaPlanPostSerializer(data=request.DATA)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

