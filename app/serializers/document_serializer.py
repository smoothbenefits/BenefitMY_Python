from rest_framework import serializers

from document_field_serializer import DocumentFieldSerializer
from app.models.document import Document
from app.models.document_field import DocumentField
import re

class DocumentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Document
        depth = 1
