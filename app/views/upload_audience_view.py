from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.http import Http404
from app.serializers.upload_audience_serializer import UploadAudienceSerializer, UploadAudiencePostSerializer
from app.models.upload_audience import UploadAudience
from app.service.hash_key_service import HashKeyService

class UploadAudienceView(APIView):
    def __init__(self):
        self.hash_service = HashKeyService()

    def _get_uploads_for_company(self, company_id):
        uploads = UploadAudience.objects.filter(company=company_id, user_for__isnull=True)
        return uploads

    def _get_uploads_for_user(self, company_id, user_id):
        uploads = UploadAudience.objects.filter(company=company_id, user_for=user_id)
        return uploads
    
    def _get_uploads_for_request(self, request, comp_id):
        user_id = self.hash_service.decode_key(request.GET.get('user_id', None))      
        upload_audience = None
        if user_id:
            upload_audience = self._get_uploads_for_user(comp_id, user_id)
        else:
            upload_audience = self._get_uploads_for_company(comp_id)
        return upload_audience

    def get(self, request, comp_id, format=None):
        upload_audience = self._get_uploads_for_request(request, comp_id)
        serialized = UploadAudienceSerializer(upload_audience, many=True)
        return Response(serialized.data)

    def post(self, request, comp_id, format=None):
        # expect upload_id to be valid
        upload_id = request.DATA.get('upload')
        if not upload_id:
            return Response({'message': 'upload is not posted with the request'}, 
                            status=status.HTTP_400_BAD_REQUEST)

        user_id = self.hash_service.decode_key(request.GET.get('user_id', None))
        serialized = UploadAudiencePostSerializer(data={'upload': upload_id, 
                                                                  'company': comp_id, 
                                                                  'user_for':user_id})
        if serialized.is_valid():
            serialized.save()
            return Response(serialized.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serialized.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, comp_id, format=None):
        upload_audience = self._get_uploads_for_request(request, comp_id)
        if upload_audience:
            for upload_item in upload_audience:
                upload_item.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
