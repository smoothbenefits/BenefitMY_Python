import json
from urlparse import urlparse
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from django.http import Http404
from datetime import datetime, timedelta
from rest_framework.response import Response
from rest_framework import status
from app.models.upload import Upload
from app.models.company_user import CompanyUser, USER_TYPE
from app.serializers.upload_serializer import UploadSerializer, UploadPostSerializer
from app.service.amazon_s3_auth import AmazonS3AuthService

_amazon_auth_service = AmazonS3AuthService()

class UserUploadView(APIView):
    def get(self, request, pk, format=None):
        try:
            user_uploads = Upload.objects.filter(user=pk)
            serialized = UploadSerializer(user_uploads, many=True)
            return Response(serialized.data)
        except Upload.DoesNotExist:
            raise Http404


    def post(self, request, pk, format=None):
        upload_data = request.DATA
        comp_id = upload_data['company']
        user_id = upload_data['user']
        file_key = _amazon_auth_service.encode_key(comp_id, user_id)
        s3_key = _amazon_auth_service.get_s3_key(upload_data['company_name'],
                                                 upload_data['file_name'],
                                                 file_key)
        upload_data.update({'S3': _amazon_auth_service.get_s3_full_url(s3_key)})
        serialized = UploadPostSerializer(data=upload_data)
        if serialized.is_valid():
            serialized.save()
            saved_upload = serialized.data
            saved_upload.update(_amazon_auth_service.get_upload_form_policy_and_signature(s3_key))
            return Response(saved_upload, status=status.HTTP_201_CREATED)
        return Response(serialized.errors, status=status.HTTP_400_BAD_REQUEST)

class UploadView(APIView):

    def _get_object(self, pk):
        try:
            return Upload.objects.get(pk=pk)
        except Upload.DoesNotExist:
            raise Http404
    

    def get(self, request,  pk, format=None):
        upload = self._get_object(pk)
        serialized = UploadSerializer(upload) 
        return Response(serialized.data)


    def delete(self, request, pk, format=None):
        upload = self._get_object(pk)
        s3 = upload.S3
        parsed_s3 = urlparse(s3)
        file_path = parsed_s3.path
        cur_time = _amazon_auth_service.get_s3_request_datetime()
        auth = _amazon_auth_service.get_s3_request_auth("DELETE", "", file_path, cur_time)
        if upload:
            upload.delete()
            return Response({'auth':auth, 'S3':s3, 'time': cur_time})
        return Response(status=status.HTTP_404_NOT_FOUND)

@api_view(['GET'])
def get_company_uploads(request, comp_id, pk, format=None):
    # We need to do some validation on the request itself.
    admin_id = request.user.id

    # Validate the current user is an admin of the company specified
    try:
        comp_users = CompanyUser.objects.get(company=comp_id, user=admin_id, company_user_type="admin")
    except CompanyUser.DoesNotExist:
        return Response({'message': 'The company and the current user do not match'}, status=405)
    
    # Validate the employee id provided is an employee of the company specified
    try:
        employee_users = CompanyUser.objects.get(company=comp_id, user=pk, company_user_type="employee")
    except CompanyUser.DoesNotExist:
        return Response({'message': 'The company and the employee do not match'}, status=405)        

    uploads = Upload.objects.filter(company=comp_id, user=pk)
    serialized = UploadSerializer(uploads, many=True)
    return Response(serialized.data) 

