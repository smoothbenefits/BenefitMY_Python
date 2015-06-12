from rest_framework import serializers

from document_field_serializer import DocumentFieldSerializer
from app.models.document import Document
from app.models.document_field import DocumentField
from company_serializer import ShallowCompanySerializer
from user_serializer import UserSerializer
from document_type_serializer import DocumentTypeSerializer
from signature_serializer import SignatureSerializer
from hash_pk_serializer_base import HashPkSerializerBase
import re


class DocumentSerializer(HashPkSerializerBase):

    company = ShallowCompanySerializer()
    user = UserSerializer()
    document_type = DocumentTypeSerializer()
    signature = SignatureSerializer()

    class Meta:
        model = Document
        fields = (  'id',
                    'company',
                    'user',
                    'document_type',
                    'signature',
                    'name',
                    'edited',
                    'content',
                    'created_at',
                    'updated_at')
