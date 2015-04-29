from rest_framework import serializers
from app.models.fsa.fsa import FSA
from ..hash_pk_serializer_base import HashPkSerializerBase
from ..custom_fields.hash_field import HashField


class FsaSerializer(HashPkSerializerBase):

	user = HashField(source="user.id")

	class Meta:
		model = FSA


class FsaPostSerializer(HashPkSerializerBase):
	
	class Meta:
		model = FSA
