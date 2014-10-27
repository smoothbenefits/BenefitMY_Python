from rest_framework.views import APIView
from django.http import Http404
from rest_framework.response import Response
from rest_framework import status

from app.models.template import Template
from app.serializers.template_serializer import (
    TemplateSerializer,
    TemplatePostSerializer)


class TemplateView(APIView):
    def get_object(self, pk):
        try:
            return Template.objects.get(pk=pk)
        except Template.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        template = self.get_object(pk)
        serializer = TemplateSerializer(template)
        return Response({'template':serializer.data})

    def post(self, request, pk, format=None):
        serializer = TemplatePostSerializer(data=request.DATA)
        if serializer.is_valid():
            serializer.save()
            return Response({'template':serializer.data}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
