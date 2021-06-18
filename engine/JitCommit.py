from .JitObject import JitObject
from .utils import kvlm_parse, kvlm_serialize
class JitCommit(JitObject):
	fmt = b'commit'

	def deserialize(self, data):
		self.kvlm = kvlm_parse(data)
	
	def serialize(self):
		return kvlm_serialzie(self.kvlm)