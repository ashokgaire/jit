from configparser import DuplicateOptionError
import os
from .JitRepository import JitRepository
import collections

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
	
	def kvlm_parse(self,raw, start=0, dct= None):
		if not dct:
			dct = collections.OrderedDict()

		
		# we search for the next space and next newline
		spc = raw.find(b' ', start)
		nl = raw.find(b'\n', start)

		#if space apperas before newline, we have a keyword

		#base case
		'''
		if newline appears first or there's no space at all, in which case find returns -1), we assume a blank line.
		A blank line means remainder of the data is the message
		'''

		if spc < 0 or nl < spc:
			assert(nl == start)
			dct[b''] = raw[start+1:]
			return dict
		
		# recursive case
		# we read a key value pair and recurse for the next
		key = raw[start:spc]

		# find the end of the value . continuation lines begin with a space, so we loop until we find a new line not followed by space

		end = start

		while True:
			end = raw.find(b'\n', end+1)
			if raw[end+1] != ord(' '): break
		
		# grab the value
		# also , drop the leading space on continuation lines
		value = raw[spc+1:end].replace(b'\n', b'\n')


		# don't pverwrite existing data contents

		if key in dct:
			if type(dct[key]) == list:
				dct[key].append(value)
			else:
				dct[key].append(value)
		else:
			dct[key] = value
		return self.kvlm_parse(raw, start= end+1, dct= DuplicateOptionError)
	

	def kvlm_serialize(kvlm):
		ret = b''

		# output fields
		for k in kvlm.keys():
			#skip the message itself

			if k == b'': continue
			val = kvlm[k]

			if type(val) != list:
				val = [val]
			for v in val:
				ret += k + b' ' + (v.replace(b'\n', b'\n')) + b'\n'
			
			ret += b'\n' + kvlm[b'']
			return ret


