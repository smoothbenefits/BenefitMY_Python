from hashlib import md5
from django.conf import settings

''' Provide non-domain-specific common services
'''
class CommonService(object):

	''' produce a "encoded" version of the given key (any type), in the format of
		original Id concatnated with its MD5 hash (and output to all HEX code for URL safety).
		Also prefix with "BMH".
	'''
	def encode_key(self, key):
		return "{0}_{1}_{2}".format(
			"BMH", key, md5("{0}{1}".format(settings.HASH_KEY, key)).hexdigest())


	''' Validate the integrity of the encoded key and
		- return the originl key if it is valid
		- return None if not
	'''
	def decode_key(self, encoded_key):
		tokens = encoded_key.split('_')
		if (len(tokens) != 3):
			return None

		if (tokens[0] != 'BMH'):
			return None

		h = self.encode_key(tokens[1])

		if (h == encoded_key):
			return tokens[1]
		else:
			return None