import os
import configparser

class JitRepository(object):
	""" A Jit Repository """

	worktree = None
	jitdir = None
	conf = None

	def __init__(self,path,force= False):
		self.worktree = path
		self.jitdir = os.path.join(path, ".jit")
		

		if not (force or os.path.isdir(self.getdir)):
			raise Exception("Not a jit repository %s" %path)

		# read configuration file in .jit/config
		self.conf = configparser.ConfigParser()
		cf = self.repo_file("config")

		if cf and os.path.exists(cf):
			self.conf.read([cf])
		elif not force:
			raise Exception("Configuration file missiing")
		
		if not force:
			vers = int(self.conf.get("core", "repositoryformatversion"))
			
			if vers !=0:
				raise Exception("Unsupported repositoryformatversion %s" % vers)
	
	def repo_path(self, *path):
		
		""" compute path under repo's jitdir. """
		return os.path.join(self.jitdir, *path)
	
	def repo_file(self, *path, mkdir= False):
		""" same as repo_path , but create dirname(*path) if absent,
		repo_file('"refs\", \"remotes\", \"origin", \"Head\") will create .jit/refs/remote/origin.
		"""

		if self.repo_dir( *path[:-1], mkdir= mkdir):
			return self.repo_path(*path)
	
	def repo_dir(self, *path, mkdir=False):
		""" same as repo_path but mkdir *path if absent"""

		path = self.repo_path(*path)

		if os.path.exists(path):
			if os.path.isdir(path):
				return path
			else:
				raise Exception("Not a directory %s" %path)
		if mkdir:
			os.makedirs(path)
			return path
		else:
			return None
	def repo_default_config(self):
		ret = configparser.ConfigParser()

		ret.add_section("core")
		ret.set("core", "repositoryformatversion", "0")
		ret.set("core", "filemode", "false")
		ret.set("core", "bare", "false")

		return ret
	