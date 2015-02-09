from rest_framework import serializers
from app.service.common_service import CommonService

""" A custom serializer field that automatically
	hash the field value based on the connical
	method.
"""
class HashField(serializers.Field):

	def to_native(self, obj):
		common_service = CommonService()
		return common_service.encode_key(obj)

	def from_native(self, data):
		common_service = CommonService()
		return common_service.decode_key(data)

