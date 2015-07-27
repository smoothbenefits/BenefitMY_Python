from rest_framework import serializers
from app.service.hash_key_service import HashKeyService

""" A custom serializer field that automatically
	hash the field value based on the canonical
	method.
"""
class HashField(serializers.Field):

	def to_native(self, obj):
		hash_key_service = HashKeyService()
		return hash_key_service.encode_key(obj)

	def from_native(self, data):
		hash_key_service = HashKeyService()
		return hash_key_service.decode_key(data)
