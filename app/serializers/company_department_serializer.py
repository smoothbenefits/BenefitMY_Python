from rest_framework import serializers
from custom_fields.hash_field import HashField
from hash_pk_serializer_base import HashPkSerializerBase

from app.models.company_department import CompanyDepartment


class CompanyDepartmentSerializer(HashPkSerializerBase):
    company = HashField(source="company.id")

    class Meta:
        model = CompanyDepartment


class CompanyDepartmentPostSerializer(serializers.ModelSerializer):

    class Meta:
        model = CompanyDepartment

class CompanyDepartmentFieldWithId(serializers.WritableField):
    def to_native(self, obj):
        if obj:
            return obj.id
        else:
            return None


    def from_native(self, data):
        if not data:
            return None
        elif isinstance(data, unicode):
            return CompanyDepartment.objects.get(id=int(data))
        else:
            comp_department = None
            if "id" not in data:
                comp_department = CompanyDepartmentSerializer(data=data)
            else:
                try:
                    dept_object = CompanyDepartment.objects.get(id=data['id'])
                    comp_department = CompanyDepartmentSerializer(dept_object, data=data)
                except CompanyDepartment.DoesNotExist:
                    comp_department = CompanyDepartmentSerializer(data=data)
            if comp_department and comp_department.is_valid():
                comp_department.save()
                return comp_department.object
            else:
                raise ValueError('Bad Company Department value')
