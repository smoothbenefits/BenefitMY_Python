from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.http import Http404
from app.models.fsa.fsa import FSA
from app.serializers.fsa.fsa_serializer import (FsaSerializer, FsaPostSerializer)

class FsaView(APIView):
    def _get_object(self, pk):
        try:
            return FSA.objects.get(pk=pk)
        except FSA.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        fsa = self._get_object(pk)
        serializer = FsaSerializer(fsa)
        return Response(serializer.data)

    def post(self, request, pk, format=None):
        serializer = FsaPostSerializer(data=request.DATA)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk, format=None):
        fsa = self._get_object(pk)
        serializer = FsaPostSerializer(fsa, data=request.DATA)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        fsa = self._get_object(pk)
        fsa.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class FSAByUserView(APIView):
    def _get_object(self, user_id):
        try:
            return FSA.objects.get(user=user_id)
        except FSA.DoesNotExist:
            raise Http404

    def get(self, request, user_id, format=None):
        fsa = self._get_object(user_id)
        serializer = FsaSerializer(fsa)
        return Response(serializer.data)
