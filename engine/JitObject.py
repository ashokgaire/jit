import hashlib
import zlib
class GitObject(object):
	repo = None

	def __init__(self, repo , data = None):
		self.repo = repo
		if data != None:
			self.deserialize(data)
	
	def serialize(self):

		raise Exception("Unimplemented !")

	def serialize(self):

		raise Exception("Unimplemented !")
	
	def object_read(self, sha):
		""" Read object object_id from jit repository repo.
		Return a JitObject whose exact type depends on the objects."""
		
		path = self.repo.repo_file( "objects", sha[0:2], sha[2:])

		with open(path, "rb") as f:
			raw = zlib.decompress(f.read())


			# Read object Type
			x = raw.find(b' ')
			fmt = raw[0:x]


			# Read and validate object sie
			y = raw.find(b'\x00', x)
			size = int(raw[x:y].decode("ascii"))

			if size != len(raw) - y-1:
				raise Exception("Malformed object {0}: bad Length".format(sha))
			

			#Pick constructor

			if fmt == b'commit' : c = JitCommit
			elif fmt == b'tree' : c = JitTree
			elif fmt == b'tag' :  c = Gittag
			elif fmt == b'blob' : c= JitBlob

			else:
				raise Exception("unknown type %s for object % s".format(fmt.decode("ascii"), sha))
			
			return c(self.repo, raw[y+1:])


		def object_write(self, obj, actually_write = True):
			#serialize object data
			data = obj.serialize()

			# add header
			result = obj.fmt + b'' + str(len(data)).encode() + b'\x00' + data

			# compute hash 
			sha = hashlib.sha1(result).hexdigest()

			if actually_write:
				#compute path 
				path = self.repo.repo_file("objects", sha[0:2], sha[2:], mkdir= actually_write)

				with open(path, 'wb') as f:
					f.write(zlib.compress(result))
			return sha

	def object_find(self, name, fmt = None, follow = True):
		return name
			

