from app.service.common_service import CommonService
from django.http import Http404

class HashPkValidationMiddleware(object):

	def process_view(self, request, view_func, view_args, view_kwargs):
		
		''' Don't like this much at all. We have to know the view arg names
			and to hard code in here, in order for the middle ware to know 
			the ids needing "decoding". But how else we could wire these
			up given the current setup??

			This is another push to think about actually using non-int 
		''' 
		self._decode_key(view_kwargs, 'pk')
		self._decode_key(view_kwargs, 'pd')
		self._decode_key(view_kwargs, 'py')
		return None

	def _decode_key(self, view_kwargs, key_name):
		if (key_name in view_kwargs):
			common_service = CommonService()
			k = common_service.decode_key(view_kwargs[key_name])
			if (not k):
				raise Http404
			view_kwargs[key_name] = k
	