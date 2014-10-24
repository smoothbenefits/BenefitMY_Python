from rest_framework import serializers
from app.models.document_field import DocumentField


class DocumentFieldSerializer(serializers.ModelSerializer):

    class Meta:
        model = DocumentField

