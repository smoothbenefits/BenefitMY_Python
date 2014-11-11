from rest_framework.views import APIView
from django.http import Http404
from rest_framework.response import Response

from app.models.document import Document
from app.serializers.document_serializer import TemplateDtypeSerializer


class CompanyTemplatesView(APIView):
    def get_templates(self, pk):
        try:
            return Document.objects.filter(company=pk)
        except Document.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        templates = self.get_templates(pk)
        serializer = TemplateDtypeSerializer(templates, many=True)
        return Response({'templates': serializer.data})
