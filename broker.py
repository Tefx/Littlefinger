class Sub(object):
	def __init__(self, desc, port):
		self.test = lambda x: eval(desc, {}, x)
		self.port = port

	def push(self, obj):
		return self.test(obj) and self.port.write(obj)

class Broker(object):
	def __init__(self):
		self.subs = []

	def push(self, data):
		self.subs = filter(lambda x: x.push(data), self.subs)

	def add_sub(self, desc, port):
		self.subs.append(Sub(desc, port))
