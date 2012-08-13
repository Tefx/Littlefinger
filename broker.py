class Sub(object):
	def __init__(self, desc, port):
		self.desc = desc
		self.test = lambda x: eval(desc, {}, x)
		self.port = port

	def push(self, obj):
		if self.test(obj):
			try:
				self.port.write(obj)
				return True
			except:
				self.port.close()
				return False

	def __repr__(self):
		return "{%s|%s}" % (self.desc, str(self.port))

class Broker(object):
	def __init__(self):
		self.subs = []

	def push(self, data):
		z = []
		for s in self.subs:
			if not s.push(data):
				z.append(s)
		for s in z:
			self.subs.remove(s)
		#self.subs = [s for s in self.subs if s.push(data)]

	def add_sub(self, desc, port):
		self.subs.append(Sub(desc, port))
