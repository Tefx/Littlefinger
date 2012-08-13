import yajl as json
import broker
from port import Port
import gevent
import gevent.socket as socket
# import json
# import socket

def loads(bytes):
    return {a:b for a,b in json.loads(bytes)}

def dumps(data):
    return json.dumps([(a,b) for a,b in data.items()])


class Server(object):
    def __init__(self):
        self.broker = broker.Broker()

    def run(self, listen_port):
        self.listen_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.listen_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.listen_socket.bind(("", listen_port))
        self.listen_socket.listen(10000)
        while True:
            sock, addr = self.listen_socket.accept()
            # self.handle(Port(sock, loads, dumps))
            gevent.spawn(self.handle, Port(sock, loads, dumps))

    def handle(self, port):
        while True:
            try:
                obj = port.read()
                if not obj:
                    break
                if "_sub" in obj:
                    self.broker.add_sub(obj["_sub"], port)
                else:
                    self.broker.push(obj)
            except:
                port.close()
                break

if __name__ == '__main__':
    Server().run(50002)