#-*-coding:utf8;-*-
import re
"""
Simple but useful chatbot router!
"""

__author__ = "guangrei"
__version__ = "v0.0.1"
_data = {}
_data_user = None

class group:
	def __init__(self, name):
		if name not in _data:
			_data[name] = {}
			_data[name]["/help"] = {}
			_data[name]["/help"]["callback"] = self._help
			_data[name]["/help"]["description"] = "show help commands"
			_data[name]["/help"]["strict"] = True
		self.id = name
			
	def add_command(self,  method, description="", strict=False):
		method = self.compile(method)
		def dec(func):
			_data[self.id][method] = {}
			_data[self.id][method]["callback"] = func
			_data[self.id][method]["description"] = description
			_data[self.id][method]["strict"] = strict
			return func
		return dec
	
	def add_default_command(self):
		def dec(func):
			_data[self.id]["__default__"] = {}
			_data[self.id]["__default__"]["callback"] = func
			return func
		return dec
	
	def compile(self, string):
		pattern = re.sub(r'\{([^}]+)\}', r'(.*)', string)
		return pattern.strip()
		
	def _help(self):
		"""
		Only list public command (command starts with "/" and have description)
		"""
		hasil = f"""Router group: {self.id}
List public commands:
"""
		i = 1
		for k,v in _data[self.id].items():
			if k.startswith("/") and len(v["description"]):
				hasil = hasil + f'{i}. {k} - {v["description"]}\n'
				i=i+1
		return hasil.strip()

def get_func(group, route):
	return _data[group][route]["callback"]

def _search(pattern, string, strict):
	if strict:
		match = re.match(pattern, string.strip())
	else:
		match = re.match(pattern, string.strip(), re.IGNORECASE)
	if match:
		return list(match.groups())
	else:
		return False

def update_data(data):
	_data_user = data

def get_data():
	return _data_user

def run(route, msg):
	
	if len(msg):
		for k,v in _data[route.id].items():
			if k != "__default__":
				args = _search(k, msg, v["strict"])
				if args is not False:
					return v["callback"](*args)
	if "__default__" in _data[route.id]:
		return _data[route.id]["__default__"]["callback"](msg)
	else:
		return f"info: no default handler for route {route.id}:{msg}!"

if __name__ == '__main__':
	g = group("testting")
	print(run(g,"/help"))