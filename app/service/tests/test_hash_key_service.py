# test document
# tests can be kicked off by running "python manage.py test app/tests/"
from django.test import TestCase
from app.service.hash_key_service import HashKeyService
import re

# Create your tests here.
class TestHashKeyService(TestCase):

	hash_key_service = HashKeyService()

	''' encode a 'None' key, should return None
	'''
	def test_Encode_NoneKey_None(self):
		key = None
		encodedKey = self.hash_key_service.encode_key(key)
		self.assertTrue(not encodedKey)


	''' encode a valid key is expected to yield result with valid token format
	'''
	def test_Encode_Key_ValidFormat(self):
		key = 20
		encodedKey = self.hash_key_service.encode_key(key)
		regex = re.compile(HashKeyService.HASH_TOKEN_REGEX_PATTERN)
		self.assertTrue(not regex.match(encodedKey) == None)


	''' decode a 'None' key, should return None
	'''
	def test_Decode_NoneKey_None(self):
		encodedkey = None
		key = self.hash_key_service.decode_key(encodedkey)
		self.assertTrue(not key)


	''' decode an invalid key, should return None
	'''
	def test_Decode_InvalidKey_None(self):
		encodedkey = 'This_Is_A_Bad_Token'
		key = self.hash_key_service.decode_key(encodedkey)
		self.assertTrue(not key)


	''' encode a valid key then decode it, should return original key
	'''
	def test_EncodeAndDecode_Key_OriginalKey(self):
		key = 20
		encodedKey = self.hash_key_service.encode_key(key)
		decodedKey = self.hash_key_service.decode_key(encodedKey)
		self.assertEqual(str(key), str(decodedKey))

