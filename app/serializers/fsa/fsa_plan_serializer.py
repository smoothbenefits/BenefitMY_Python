from rest_framework import serializers
from app.models.fsa.fsa_plan import FsaPlan
from ..hash_pk_serializer_base import HashPkSerializerBase
from ..custom_fields.hash_field import HashField

class FsaPlanSerializer(HashPkSerializerBase):
    broker_user = HashField(source="broker_user.id")

    class Meta:
        model = FsaPlan


class FsaPlanPostSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = FsaPlan
