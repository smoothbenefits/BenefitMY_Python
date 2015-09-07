from rest_framework.views import APIView
from rest_framework.response import Response

from app.service.account_creation_service import AccountCreationService
from app.serializers.dtos.batch_account_creation_raw_data_serializer import BatchAccountCreationRawDataSerializer
from app.serializers.dtos.batch_account_creation_raw_data_parse_result_serializer \
    import BatchAccountCreationRawDataParseResultSerializer


class AccountInfoListParseView(APIView):
    def post(self, request, company_id, format=None):
        serializer = BatchAccountCreationRawDataSerializer(data=request.DATA)
        if (not serializer.is_valid()):
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        raw_data = serializer.object
        raw_data.company_id = company_id

        service = AccountCreationService()
        parse_result = service.parse_raw_data(raw_data)

        result_serializer = BatchAccountCreationRawDataParseResultSerializer(parse_result)

        return Response(result_serializer.data)
