from rest_framework.views import APIView
from django.http import Http404
from rest_framework.response import Response
from django.db import transaction
from rest_framework import status
from rest_framework.decorators import api_view


from app.models.benefit_details import BenefitDetails
from app.models.benefit_policy_key import BenefitPolicyKey
from app.models.benefit_policy_type import BenefitPolicyType
from app.serializers.benefit_details_serializer import BenefitDetailsSerializer


class BenefitDetailsView(APIView):
    def get_object(self, plan_id):
        try:
            return BenefitDetails.objects.filter(benefit_plan=plan_id).order_by('benefit_policy_type_id', 
                                                                                'benefit_policy_key_id')
        except BenefitDetails.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        details = self.get_object(pk)
        serializer = BenefitDetailsSerializer(details, many=True)
        return Response(serializer.data)

    @transaction.atomic
    def post(self, request, pk, format=None):
        try:
            key = BenefitPolicyKey.objects.get(name=request.DATA['key'])
        except BenefitPolicyKey.DoesNotExist:
            key = BenefitPolicyKey(name=request.DATA['key'])
            key.save()

        try:
            t = BenefitPolicyType.objects.get(name=request.DATA['type'])
        except BenefitPolicyType.DoesNotExist:
            t = BenefitPolicyType(name=request.DATA['type'])
            t.save()

        try:
            detail = BenefitDetails.objects.get(
                benefit_policy_key=key,
                benefit_policy_type=t,
                benefit_plan_id=request.DATA['benefit_plan_id'])

            if detail.value == request.DATA['value']:
                return Response(status=status.HTTP_409_CONFLICT)
            else:
                detail.value = request.DATA['value']
                detail.save()
                serializer = BenefitDetailsSerializer(detail)
                return Response(serializer.data)

        except BenefitDetails.DoesNotExist:

            detail = BenefitDetails(
                benefit_policy_key=key,
                benefit_policy_type=t,
                benefit_plan_id=request.DATA['benefit_plan_id'],
                value=request.DATA['value'])
            detail.save()
            serializer = BenefitDetailsSerializer(detail)
            return Response(serializer.data)


@api_view(['DELETE'])
def delete_benefit_details(request, pk):

    try:
        detail = BenefitDetails.objects.get(pk=pk)
    except BenefitDetails.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'DELETE':
        detail.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
