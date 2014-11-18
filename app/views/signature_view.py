from rest_framework.views import APIView
from django.http import Http404
from rest_framework import status

from app.models.signature import Signature
from app.serializers.signature_serializer import SignatureSerializer
from rest_framework.response import Response


class SignatureView(APIView):
    def _get_object(self, pk):
        try:
            return Signature.objects.get(user=pk)
        except Signature.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        s = self._get_object(pk)
        serializer = SignatureSerializer(s)
        return Response(serializer.data)

    def post(self, request, pk, format=None):

        request.DATA['user'] = pk
        try:
            s = Signature.objects.get(user=pk)
            serializer = SignatureSerializer(s, data=request.DATA)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Signature.DoesNotExist:
            serializer = SignatureSerializer(data=request.DATA)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
