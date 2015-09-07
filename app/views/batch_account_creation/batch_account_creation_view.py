from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db import transaction

from app.service.account_creation_service import AccountCreationService
from app.serializers.dtos.account_creation_data_serializer import AccountCreationDataSerializer
from app.serializers.dtos.batch_account_creation_result_serializer import BatchAccountCreationResultSerializer


class BatchAccountCreationView(APIView):

    @transaction.atomic
    def post(self, request, company_id, format=None):
        serializer = AccountCreationDataSerializer(data=request.DATA, many=True)
        if (not serializer.is_valid()):
            print serializer.errors
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        account_data_list = serializer.object

        service = AccountCreationService()
        creation_result = service.execute_creation_batch(account_data_list)

        result_serializer = BatchAccountCreationResultSerializer(creation_result)

        return Response(result_serializer.data)
