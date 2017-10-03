from rest_framework import serializers
from custom_fields.hash_field import HashField
from hash_pk_serializer_base import HashPkSerializerBase

from app.models.company_division import CompanyDivision


class CompanyDivisionSerializer(HashPkSerializerBase):
    company = HashField(source="company.id")

    class Meta:
        model = CompanyDivision


class CompanyDivisionPostSerializer(serializers.ModelSerializer):

    class Meta:
        model = CompanyDivision

class CompanyDivisionFieldWithId(serializers.WritableField):
    def to_native(self, obj):
        print "the division field to_native got object {}, with type {}".format(obj, type(obj))
        if isinstance(obj, int):
            return obj
        elif obj:
            return obj.id
        else:
            return None


    def from_native(self, data):
        print "the division field from_native got object {}, with type {}".format(data, type(data))
        if not data:
            return None
        elif isinstance(data, unicode):
            return CompanyDivision.objects.get(id=int(data))
        else:
            comp_division = None
            if "id" not in data:
                comp_division = CompanyDivisionSerializer(data=data)
            else:
                try:
                    division_object = CompanyDivision.objects.get(id=data['id'])
                    comp_division = CompanyDivisionSerializer(division_object, data=data)
                except CompanyDivision.DoesNotExist:
                    comp_division = CompanyDivisionSerializer(data=data)
            if comp_division and comp_division.is_valid():
                comp_division.save()
                return comp_division.object
            else:
                raise ValueError('Bad Company Division value')
