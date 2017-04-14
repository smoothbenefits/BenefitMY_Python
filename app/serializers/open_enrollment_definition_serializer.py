from app.serializers.company_serializer import ShallowCompanySerializer
from app.models.open_enrollment_definition import OpenEnrollmentDefinition
from hash_pk_serializer_base import HashPkSerializerBase


class OpenEnrollmentDefinitionSerializer(HashPkSerializerBase):
    company = ShallowCompanySerializer()
    class Meta:
        
        model = OpenEnrollmentDefinition
        fields = ('id',
                  'company',
                  'start_month',
                  'start_day',
                  'end_month',
                  'end_day')


class OpenEnrollmentDefinitionPostSerializer(HashPkSerializerBase):

    class Meta:

        model = OpenEnrollmentDefinition
        fields = ('id',
                  'company',
                  'start_month',
                  'start_day',
                  'end_month',
                  'end_day')
