from app.models.company_group import CompanyGroup

from hash_pk_serializer_base import HashPkSerializerBase
from company_serializer import ShallowCompanySerializer

class CompanyGroupSerializer(HashPkSerializerBase):

    company = ShallowCompanySerializer()
    class Meta:
        model = CompanyGroup

class CompanyGroupPostSerializer(HashPkSerializerBase):

    class Meta:
        model = CompanyGroup
