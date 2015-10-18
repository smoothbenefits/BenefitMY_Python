from rest_framework.views import APIView
from django.http import Http404
from rest_framework import status

from django.db import transaction
from app.models.signature import Signature
from app.serializers.signature_serializer import (
    SignatureSerializer,
    SignaturePostSerializer)
from rest_framework.response import Response


class SignatureView(APIView):
    def _get_object(self, pk):
        try:
            return Signature.objects.get(pk=pk)
        except Signature.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        s = self._get_object(pk)
        serializer = SignatureSerializer(s)
        return Response(serializer.data)

    @transaction.atomic
    def post(self, request, format=None):
        serializer = SignaturePostSerializer(data=request.DATA)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SignatureByUserView(APIView):
    def _get_object(self, user_id):
        try:
            signature_list = Signature.objects.filter(user=user_id)
            if signature_list:
                return signature_list[0]
            else:
                return None
        except Signature.DoesNotExist:
            raise Http404

    def get(self, request, user_id, format=None):
        s = self._get_object(user_id)
        if s:
            serializer = SignatureSerializer(s)
            return Response(serializer.data)
        else:
            return Response({})
