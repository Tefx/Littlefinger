from port import Port
import yajl as json
import json
import socket


def test(k):
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	sock.connect(("localhost", 50002))

	port = Port(sock, json.loads, json.dumps)

	#s = [("_sub", "c<0")]
	#port.write(s)

	a = [("a", "sadf"), ("b", 10), ("c", -6)]

	for i in xrange(k):
		port.write(a)
		#port.read()

	port.close()


for i in xrange(1):
	test(100000)