from rest_framework.views import APIView
from django.http import Http404
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.db import transaction
from rest_framework import status
import re

from app.models.signature import Signature
from app.models.document_type import DocumentType
from app.models.document import Document
from app.models.template import Template
from app.serializers.document_serializer import (
    DocumentSerializer)
from app.serializers.dtos.key_value_pair_serializer import KeyValuePairSerializer
from app.service.template_service import TemplateService


class DocumentView(APIView):
    def get_documents(self, pk):
        try:
            return Document.objects.get(pk=pk)
        except Document.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        document = self.get_documents(pk)
        serializer = DocumentSerializer(document)
        return Response(serializer.data)

    def delete(self, request, pk, format=None):
        d = self.get_documents(pk)
        d.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def put(self, request, pk, format=None):
        """ only allow to update document name and content"""

        d = self.get_documents(pk)
        if request.DATA['document']['name']:
            d.name = request.DATA['document']['name']
        if request.DATA['document']['content']:
            d.content = request.DATA['document']['content']
        d.save()
        serializer = DocumentSerializer(d)
        return Response(serializer.data)


class CompanyDocumentView(APIView):
    def get_documents(self, pk):
        try:
            return Document.objects.filter(company=pk)
        except Document.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        documents = self.get_documents(pk)
        serializer = DocumentSerializer(documents, many=True)
        return Response(serializer.data)


class CompanyUserDocumentView(APIView):
    def get_documents(self, pk, pd):
        try:
            return Document.objects.filter(company=pk, user=pd)
        except Document.DoesNotExist:
            raise Http404

    def get(self, request, pk, pd, format=None):
        documents = self.get_documents(pk, pd)
        serializer = DocumentSerializer(documents, many=True)
        return Response(serializer.data)


class CompanyUserTypeDocumentView(APIView):
    def get_documents(self, pk, pd, py):
        try:
            return Document.objects.filter(company=pk,
                                           user=pd,
                                           document_type=py)
        except Document.DoesNotExist:
            raise Http404

    def get(self, request, pk, pd, py, format=None):
        documents = self.get_documents(pk, pd, py)
        serializer = DocumentSerializer(documents, many=True)
        return Response(serializer.data)


class UserDocumentView(APIView):
    def get_documents(self, pk):
        try:
            return Document.objects.filter(user=pk)
        except Document.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        documents = self.get_documents(pk)
        serializer = DocumentSerializer(documents, many=True)
        return Response(serializer.data)


def _generate_content(template_id, fields):
    """Generate doc content according to given template, document_type, fields
    """
    try:
        template = Template.objects.get(pk=template_id)
    except Document.DoesNotExist:
        raise Http404
    content = template.content

    template_service = TemplateService()
    fields_serializer = KeyValuePairSerializer(data=fields, many=True)
    if (not fields_serializer.is_valid()):
        raise ValueError('The given list of document fields could not be read properly.')
    return template_service.populate_content_with_field_values(content, fields_serializer.object)

@api_view(['POST'])
@transaction.atomic
def documents(request):
    s = None
    if request.DATA['signature']:
        s = Signature(signature=request.DATA['signature'],
                      user_id=request.DATA['user'])
        s.save()


    if 'template' not in request.DATA:
        d = Document(company_id=request.DATA['company'],
                     user_id=request.DATA['user'],
                     name=request.DATA['document']['name'],
                     signature=s,
                     content=request.DATA['document']['content']
                     )
    else:
        d = Document(company_id=request.DATA['company'],
                     user_id=request.DATA['user'],
                     name=request.DATA['document']['name'],
                     content=_generate_content(request.DATA['template'],
                                               request.DATA['document']['fields']),
                     signature=s
                     )

    d.save()
    serializer = DocumentSerializer(d)
    return Response(serializer.data)


class DocumentSignatureView(APIView):
    def get_document(self, pk):
        try:
            return Document.objects.get(pk=pk)
        except Document.DoesNotExist:
            raise Http404

    @transaction.atomic
    def post(self, request, pk, format=None):

        document = self.get_document(pk=pk)
        s = Signature(signature=request.DATA['signature'],
            signature_type='sign_doc',
            user_id=document.user.id)
        s.save()
        document.signature = s
        document.save()
        serialized = DocumentSerializer(document)
        return Response(serialized.data)
