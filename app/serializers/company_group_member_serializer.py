from app.models.company_group import CompanyGroup
from company_serializer import ShallowCompanySerializer
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


class CompanyGroupMemberUserSerializer(HashPkSerializerBase):

    user = UserSerializer()
    class Meta:
        model = CompanyGroupMember
        fields = ("id", "user", "created")


class CompanyGroupWithMemberSerializer(HashPkSerializerBase):

    company = ShallowCompanySerializer()
    company_group_member = CompanyGroupMemberUserSerializer(many=True)
    class Meta:
        model = CompanyGroup
        fields = ("id", "company", "name", "created", "updated", "company_group_member")
