from gevent import sleep
from port import Port
import gevent.socket as socket
from config import SERVICE_PORT
from gevent.queue import Queue
import gevent
import random

def rand(a, b):
	while True:
		yield random.uniform(a, b)

def choice(l):
	while True:
		yield random.choice(l)

def const(x):
	while True:
		yield x

def gen_auto_iter(config):
	delta = config["_delta"]
	while True:
		yield {x:y.next() for x,y in config.items() if not x == "_delta"}
		sleep(delta.next())

class Source(object):
	def __init__(self, host):
		sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		sock.connect((host, SERVICE_PORT))
		self.port = Port(sock)

	def sendall(self, list):
		for item in list:
			self.port.write(item)

	def send(self, item):
		self.port.write(item)

class Receiver(object):
	def __init__(self, subs, addr):
		self.subs = {"_sub":subs}
		self.queue = Queue()
		self.listenlet = gevent.spawn(self.listen, addr)

	def listen(self, host):
		sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		sock.connect((host, SERVICE_PORT))
		port = Port(sock)
		port.write(self.subs)
		while True:
			res = port.read()
			if res:
				self.queue.put(res)

	def __iter__(self):
		return self

	def next(self):
		return self.queue.get()