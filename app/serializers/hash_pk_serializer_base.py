from rest_framework import serializers
from custom_fields.hash_field import HashField

class HashPkSerializerBase(serializers.ModelSerializer):

	#id = serializers.SerializerMethodField('dummy_id')
	id = HashField()
	
	class Meta:
		abstract = True