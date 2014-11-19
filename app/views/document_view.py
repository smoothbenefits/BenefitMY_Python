from rest_framework.views import APIView
from django.http import Http404
from rest_framework.response import Response
from rest_framework.decorators import api_view


from app.models.signature import Signature
from app.models.document_field import DocumentField
from app.models.document_type import DocumentType
from app.models.document import Document
from app.serializers.document_serializer import (
    DocumentSerializer)


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


@api_view(['POST'])
def documents(request):
    s = None
    if request.DATA['signature']:
        s = Signature(signature=request.DATA['signature'],
                      user_id=request.DATA['user'])
        s.save()

    if 'template' not in request.DATA:
        try:
            d_type = DocumentType.objects.get(
                name=request.DATA['document']['document_type'])
        except DocumentType.DoesNotExist:
            d_type = DocumentType(
                name=request.DATA['document']['document_type'])

        d = Document(company_id=request.DATA['company'],
                     user_id=request.DATA['user'],
                     document_type=d_type,
                     name=request.DATA['document']['name'],
                     signature=s
                     )
        d.save()
        serializer = DocumentSerializer(d)
        return Response(serializer.data)

    else:
        try:
            d_type = DocumentType.objects.get(
                name=request.DATA['document']['document_type'])
        except DocumentType.DoesNotExist:
            d_type = DocumentType(
                name=request.DATA['document']['document_type'])

        d = Document(company_id=request.DATA['company'],
                     user_id=request.DATA['user'],
                     document_type=d_type,
                     name=request.DATA['document']['name'],
                     template_id=request.DATA['template'],
                     signature=s
                     )
        d.save()

        for field in request.DATA['document']['fields']:
            d_f = DocumentField(name=field['name'],
                                value=field['value'],
                                document=d)
            d_f.save()

        serializer = DocumentSerializer(d)
        return Response(serializer.data)


class DocumentSignatureView(APIView):
    def get_document(self, pk):
        try:
            return Document.objects.get(pk=pk)
        except Document.DoesNotExist:
            raise Http404

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



