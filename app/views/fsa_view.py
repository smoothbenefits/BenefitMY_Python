from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.http import Http404
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
        serializer = FSASerializer(fsa, many=True)
        return Response(serializer.data)

    def post(self, request, pk, format=None):
        user_id = request.DATA['user']
        person_id = request.DATA['person']
        try:
            fsa = FSA.objects.get(user=user_id, person=person_id)
            return Response(status=status.HTTP_409_CONFLICT)
        except FSA.DoesNotExist:
            serializer = FSASerializer(data=request.DATA)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk, format=None):
        fsa = self._get_object(pk)
        serializer = FSASerializer(fsa, data=request.DATA)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        f = self._get_object(pk)
        f.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
