from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.http import Http404
from app.serializers.upload_for_user_serializer import UploadForUserSerializer, UploadForUserPostSerializer
from app.models.upload_for_user import UploadForUser
from app.service.hash_key_service import HashKeyService

class UploadForUserView(APIView):
    def __init__(self):
        self.hash_service = HashKeyService()

    def _get_uploads_for_user(self, user_id):
        uploads = UploadForUser.objects.select_related('upload').filter(user_for=user_id)
        return uploads

    def get(self, request, user_id, format=None):
        uploads_for_user = self._get_uploads_for_user(user_id)
        serialized = UploadForUserSerializer(uploads_for_user, many=True)
        return Response(serialized.data)

    def post(self, request, user_id, format=None):
        # expect upload_id to be valid
        upload_id = request.DATA.get('upload')
        if not upload_id:
            return Response({'message': 'upload is not posted with the request'},
                            status=status.HTTP_400_BAD_REQUEST)

        serialized = UploadForUserPostSerializer(data = {'upload': upload_id,
                                                        'user_for':user_id})
        if serialized.is_valid():
            serialized.save()
            return Response(serialized.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serialized.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, user_id, format=None):
        uploads_for_user = self._get_uploads_for_user(user_id)
        if uploads_for_user:
            for upload_item in uploads_for_user:
                upload_item.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
