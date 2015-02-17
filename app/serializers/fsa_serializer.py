from rest_framework import serializers
from app.models.fsa import FSA
from hash_pk_serializer_base import HashPkSerializerBase
from custom_fields.hash_field import HashField


class FSASerializer(HashPkSerializerBase):

	user = HashField(source="user.id")

	class Meta:
		model = FSA


class FSAPostSerializer(HashPkSerializerBase):
	
	class Meta:
		model = FSA
