import StringIO

from rest_framework.views import APIView
from django.http import (
    HttpResponse,
    Http404,
    HttpResponseBadRequest,
    HttpResponseRedirect
)
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.db import transaction
from rest_framework import status
import re

from app.models.company_user import (CompanyUser, USER_TYPE_EMPLOYEE)
from app.models.signature import Signature
from app.models.document_type import DocumentType
from app.models.document import Document
from app.models.template import Template
from app.serializers.document_serializer import (
    DocumentSerializer)
from app.serializers.dtos.key_value_pair_serializer import KeyValuePairSerializer
from app.service.template_service import TemplateService
from app.service.signature_service import SignatureService
from app.service.web_request_service import WebRequestService


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
    def _get_documents(self, pk):
        try:
            return Document.objects.filter(company=pk)
        except Document.DoesNotExist:
            raise Http404

    def _get_template(self, template_id):
        try:
            return Template.objects.get(pk=template_id)
        except Template.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        documents = self._get_documents(pk)
        serializer = DocumentSerializer(documents, many=True)
        return Response(serializer.data)

    @transaction.atomic
    def post(self, request, pk, format=None):
        company_id = pk
        name = request.DATA['document_name']
        template_id = request.DATA['template_id']
        signature = None
        content = ''
        template = self._get_template(template_id)
        upload = template.upload

        if (not name or not upload):
            return Response(status.HTTP_400_BAD_REQUEST)

        result_data = []

        employees = CompanyUser.objects.filter(company=company_id, company_user_type=USER_TYPE_EMPLOYEE)
        for employee in employees:
            d = Document(company_id=company_id,
                         user_id=employee.user.id,
                         name=name,
                         signature=signature,
                         content=content,
                         upload_id=upload.id)
            d.save()
            serializer = DocumentSerializer(d)
            result_data.append(serializer.data)

        return Response(result_data, status=status.HTTP_201_CREATED)


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
                     content=request.DATA['document']['content'],
                     upload_id=request.DATA['document']['upload']
                     )
    else:
        d = Document(company_id=request.DATA['company'],
                     user_id=request.DATA['user'],
                     name=request.DATA['document']['name'],
                     content=_generate_content(request.DATA['template'],
                                               request.DATA['document']['fields']),
                     upload_id=request.DATA['document']['upload'],
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

    def get_signature(self, signature_id):
        try:
            return Signature.objects.get(pk=signature_id)
        except Signature.DoesNotExist:
            raise Http404

    @transaction.atomic
    def post(self, request, pk, format=None):

        document = self.get_document(pk=pk)
        signature = self.get_signature(request.DATA['signature_id'])
        document.signature = signature
        document.save()
        serialized = DocumentSerializer(document)
        return Response(serialized.data)


class DocumentDownloadView(APIView):

    def get(self, request, document_id, format=None):
        document = self._get_document(document_id)

        if (not document.upload):
            # Being asked to download a document that has no upload
            # is an invalid request
            return HttpResponseBadRequest('Specified document does not have an upload. It is not valid for download.')

        # Do the additional processing for PDF documents that has been signed
        if ('pdf' in document.upload.file_type.lower()
            and document.signature):
            web_request_service = WebRequestService()
            signature_service = SignatureService()

            # Get the PDF stream from the URL
            res = web_request_service.get(document.upload.S3)
            res.raise_for_status()
            pdf_stream = StringIO.StringIO(res.content)

            # Construct the response
            file_name = 'Signed_{}'.format(document.upload.file_name)
            response = HttpResponse(content_type='application/pdf')
            response['Content-Disposition'] = 'attachment; filename="{}"'.format(file_name)
   
            # Use the signature service to add signature page
            signature_service.append_signature_page(
                pdf_stream,
                document.user.id,
                document.updated_at,
                response
            )

            return response

        return HttpResponseRedirect(document.upload.S3)

    def _get_document(self, document_id):
        try:
            return Document.objects.get(pk=document_id)
        except Document.DoesNotExist:
            raise Http404