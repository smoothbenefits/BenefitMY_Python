from rest_framework import serializers
from ..hash_pk_serializer_base import HashPkSerializerBase
from app.models.hra.hra_plan import HraPlan

class HraPlanSerializer(HashPkSerializerBase):
    class Meta:
        model = HraPlan
