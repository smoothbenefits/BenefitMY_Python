from app.service.hash_key_service import HashKeyService

class ViewTestBase(object):

	hash_key_service = HashKeyService()

	def normalize_key(self, key):
		return self.hash_key_service.encode_key(key)
