from rest_framework import serializers
from ..custom_fields.hash_field import HashField
from ..hash_pk_serializer_base import HashPkSerializerBase

from app.models.workers_comp.company_phraseology import \
    CompanyPhraseology
from phraseology_serializer import PhraseologySerializer


class CompanyPhraseologySerializer(HashPkSerializerBase):
    phraseology = PhraseologySerializer()
    company = HashField(source="company.id")

    class Meta:
        model = CompanyPhraseology


class CompanyPhraseologyPostSerializer(serializers.ModelSerializer):

    class Meta:
        model = CompanyPhraseology
