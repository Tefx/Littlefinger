from port import Port
import gevent.socket as socket
import gevent


def test(k):
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	sock.connect(("127.0.0.1", 5000))

	port = Port(sock)

	s = {"_sub":"c<0"}
	port.write(s)

	a = {"a":"sadf", "b":10, "c":-6}

	for i in xrange(k):
		port.write(a)

	port.close()


l = []
for i in xrange(1000):
	l.append(gevent.spawn(test, 100))

gevent.joinall(l)


# test(1000)