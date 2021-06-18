import os
from .JitRepository import JitRepository

# Utility class
class Util:

	def find_repo(self,path = "", required= True):
		""" function to find a repo in prent directory"""
		path = os.path.realpath(path)
		if os.path.isdir(os.path.join(path, ".jit")):
			return JitRepository(path)
		
		# recurese until we found the realpath
		parent = os.path.realpath(os.path.join(path, ".."))
		if parent == path:
			if required:
				raise Exception("No git directory")
			else:
				return None
		return self.find_repo(parent, required)
		

