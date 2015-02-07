from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db import transaction

from app.models.fsa import FSA
from app.serializers.fsa_serializer import FSASerializer


class FSAView(APIView):
    def _get_object(self, pk):
        try:
            return FSA.objects.get(pk=pk)
        except FSA.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        fsa = FSA.objects.filter(user=pk)
        serializer = FSASerializer(fsa)
        return Response(serializer.data

    def delete(self, request, pk, format=None):
        f = self._get_object(pk)
        f.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


