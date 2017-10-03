from rest_framework import serializers
from custom_fields.hash_field import HashField
from hash_pk_serializer_base import HashPkSerializerBase

from app.models.company_job import CompanyJob


class CompanyJobSerializer(HashPkSerializerBase):
    company = HashField(source="company.id")

    class Meta:
        model = CompanyJob


class CompanyJobPostSerializer(serializers.ModelSerializer):

    class Meta:
        model = CompanyJob

class CompanyJobFieldWithId(serializers.WritableField):
    def to_native(self, obj):
        print "the job field to_native got object {}, with type {}".format(obj, type(obj))
        if isinstance(obj, int):
            return obj
        elif obj:
            return obj.id
        else:
            return None


    def from_native(self, data):
        print "the job field from_native got object {}, with type {}".format(data, type(data))
        if not data:
            return None
        elif isinstance(data, unicode):
            return CompanyJob.objects.get(id=int(data))
        else:
            comp_job = None
            if "id" not in data:
                comp_job = CompanyJobSerializer(data=data)
            else:
                try:
                    job_object = CompanyJob.objects.get(id=data['id'])
                    comp_job = CompanyJobSerializer(job_object, data=data)
                except CompanyJob.DoesNotExist:
                    comp_job = CompanyJobSerializer(data=data)
            if comp_job and comp_job.is_valid():
                comp_job.save()
                return comp_job.object
            else:
                raise ValueError('Bad Company Job value')
