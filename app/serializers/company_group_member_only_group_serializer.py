from company_group_serializer import CompanyGroupPostSerializer
from app.models.company_group_member import CompanyGroupMember
from hash_pk_serializer_base import HashPkSerializerBase

class CompanyGroupMemberOnlyGroupSerializer(HashPkSerializerBase):

    company_group = CompanyGroupPostSerializer()
    class Meta:
        model = CompanyGroupMember
        fields = ("id", "company_group")
