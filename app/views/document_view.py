from rest_framework.views import APIView
from django.http import Http404
from rest_framework.response import Response

from app.models.document import Document
from app.serializers.document_serializer import DocumentSerializer


class DocumentView(APIView):
    def get_documents(self, pk):
        try:
            return Document.objects.filter(company=pk)
        except Document.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        documents = self.get_documents(pk)
        serializer = DocumentSerializer(documents, many=True)
        return Response(serializer.data)
