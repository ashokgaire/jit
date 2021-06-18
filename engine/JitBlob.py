from .JitObject import JitObject

class GitBlob(JitObject):
	fmt = b'blob'

	def serialize(self):
		return self.blobdata
	
	def deserialize(self, data):
		self.blobdata = data
