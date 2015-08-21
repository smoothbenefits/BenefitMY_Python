from hashlib import md5
from django.conf import settings

''' Provides service to handle hash and unhash of keys
'''
class HashKeyService(object):

	''' Prefix for all hashed tokens '''
	HASH_TOKEN_PREFIX = 'BMHT'

	''' Regex pattern to match hashed tokens'''
	HASH_TOKEN_REGEX_PATTERN = r'BMHT_[0-9]+_\w+'

	''' produce a "encoded" version of the given key (any type), in the format of
		original Id concatnated with its MD5 hash (and output to all HEX code for URL safety).
		Also prefix with the HASH_TOKEN_PREFIX.
	'''
	def encode_key(self, key):
		if (not key):
			return key

		return "{0}_{1}_{2}".format(
			self.HASH_TOKEN_PREFIX, key, md5("{0}{1}".format(settings.HASH_KEY, key)).hexdigest())


	''' Validate the integrity of the encoded key and
		- return the originl key if it is valid
		- return None if not
	'''
	def decode_key(self, encoded_key):
		if (not encoded_key):
			return encoded_key

		tokens = encoded_key.split('_')
		if (len(tokens) != 3):
			return None

		if (tokens[0] != self.HASH_TOKEN_PREFIX):
			return None

		h = self.encode_key(tokens[1])

		if (h == encoded_key):
			return tokens[1]
		else:
			return None

	def is_encoded(self, value):
		try:
			decoded = decode_key(value)
			return decoded != value
		except:
			return False
