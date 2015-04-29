from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.http import Http404
from app.models.fsa.fsa import FSA
from app.serializers.fsa_serializer import (FSASerializer, FSAPostSerializer)

class FSAView(APIView):
    def _get_object(self, pk):
        try:
            return FSA.objects.get(pk=pk)
        except FSA.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        fsa = self._get_object(pk)
        serializer = FSASerializer(fsa)
        return Response(serializer.data)

    def post(self, request, pk, format=None):
        serializer = FSASerializer(data=request.DATA)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return REsponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk, format=None):
        fsa = self._get_object(pk)
        serializer = FSASerializer(fsa, data=request.DATA)
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
        fsa = _get_object(user_id)
        serializer = FSASerializer(fsa)
        return Response(serializer.data)
