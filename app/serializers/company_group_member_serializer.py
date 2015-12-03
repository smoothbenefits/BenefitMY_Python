from app.models.company_group_member import CompanyGroupMember
from hash_pk_serializer_base import HashPkSerializerBase
from company_group_serializer import CompanyGroupSerializer
from user_serializer import UserSerializer

class CompanyGroupMemberSerializer(HashPkSerializerBase):

    company_group = CompanyGroupSerializer()
    user = UserSerializer()
    class Meta:
        model = CompanyGroupMember

class CompanyGroupMemberPostSerializer(HashPkSerializerBase):

    class Meta:
        model = CompanyGroupMember
