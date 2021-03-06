from __future__ import print_function, division
import collections
import json
import copy

class PyConfDict(collections.OrderedDict):

	def __init__(self,*args,json_fn=None,**kwargs):
		if json_fn is not None:
			super(self.__class__,self).__init__({})
			self.update_from_json(json_fn,allow_new_keys=True)
		else:
			super(self.__class__,self).__init__(*args,**kwargs)

	def update(self,conf_dict,allow_new_keys=False):
		"""Update dictionary from another dictionary.
		"""
		old_keys=set(self.keys())
		#super(self.__class__, self).update(conf_dict)
		for key in conf_dict.keys():
			self[key]=copy.deepcopy(conf_dict[key])
		new_keys=set(self.keys())
		keys_diff=new_keys-old_keys
		if not allow_new_keys:
			if keys_diff!=set():
				exception_message="Adding new keys during update: {}".format(", ".join(keys_diff))
				raise ValueError(exception_message)

	def update_from_json(self,json_fn,allow_new_keys=False):
		"""Update from a JSON file.
		"""
		with open(json_fn) as json_fo:
			conf_dict=json.loads(json_fo.read())
		self.update(conf_dict=conf_dict,allow_new_keys=allow_new_keys)
			
	def fill_missing(self,conf_dict):
		"""Add (key,value) for missing keys.
		"""
		self_keys=self.keys()
		for key in conf_dict.keys():
			if key not in self_keys:
				self[key]=conf_dict[key]
	
	def fill_missing_from_json(self,json_fn):
		"""Fill missing values from a JSON file.
		"""
		with open(json_fn) as json_fo:
			conf_dict=json.loads(json_fo.read())
		self.fill_missing(conf_dict=conf_dict,allow_new_keys=allow_new_keys)

	def save_to_json(self,json_fn):
		"""Save to a JSON file.
		"""
		with open(json_fn,"w+") as json_fo:
			json.dump(self,json_fo,sort_keys=False, indent=4)

