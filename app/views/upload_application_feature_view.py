from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.http import Http404
from app.serializers.upload_application_feature_serializer import UploadApplicationFeatureSerializer, UploadApplicationFeaturePostSerializer
from app.models.upload_application_feature import UploadApplicationFeature


class UploadApplicationFeatureView(APIView):
    def _get_uploads(self, application_feature, feature_id):
        uploads = UploadApplicationFeature.objects.filter(feature_id=feature_id, application_feature=application_feature)
        return uploads

    # PK is always the sys_application_feature_id
    def get(self, request, pk, feature_id, format=None):
        uploads = self._get_uploads(pk, feature_id)
        serialized = UploadApplicationFeatureSerializer(uploads, many=True)
        return Response(serialized.data)

    def post(self, request, pk, feature_id, format=None):
        # expect upload_id to be valid
        upload_id = request.DATA.get('upload')
        if not upload_id:
            return Response({'message': 'upload is not posted with the request'}, 
                            status=status.HTTP_400_BAD_REQUEST)

        serialized = UploadApplicationFeaturePostSerializer(data={'upload': upload_id, 
                                                                  'application_feature': pk, 
                                                                  'feature_id':feature_id})
        if serialized.is_valid():
            serialized.save()
            return Response(serialized.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serialized.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, feature_id, format=None):
        uploads = self._get_uploads(pk, feature_id)
        if uploads:
            for upload_item in uploads:
                upload_item.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
