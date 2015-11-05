from rest_framework import serializers

from document_field_serializer import DocumentFieldSerializer
from app.models.document import Document
from app.models.document_field import DocumentField
from company_serializer import ShallowCompanySerializer
from user_serializer import UserSerializer
from signature_serializer import SignatureSerializer
from upload_serializer import UploadSerializer
from hash_pk_serializer_base import HashPkSerializerBase
import re


class DocumentSerializer(HashPkSerializerBase):

    company = ShallowCompanySerializer()
    user = UserSerializer()
    signature = SignatureSerializer()
    upload = UploadSerializer()

    class Meta:
        model = Document
        fields = (  'id',
                    'company',
                    'user',
                    'signature',
                    'name',
                    'edited',
                    'content',
                    'upload',
                    'created_at',
                    'updated_at')
