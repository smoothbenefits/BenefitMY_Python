from rest_framework.views import APIView
from rest_framework.response import Response

from app.models.document_type import DocumentType
from app.serializers.document_type_serializer import DocumentTypeSerializer


class DocumentTypeView(APIView):

    def get(self, request, format=None):
        types = DocumentType.objects.all()
        serializer = DocumentTypeSerializer(types, many=True)
        return Response(serializer.data)
