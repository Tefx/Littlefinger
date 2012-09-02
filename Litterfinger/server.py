import broker
from port import Port
import gevent
import gevent.socket as socket
from config import SERVICE_PORT

class Server(object):
    def __init__(self):
        self.broker = broker.Broker()

    def run(self, listen_port=SERVICE_PORT):
        self.listen_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # self.listen_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.listen_socket.bind(("", listen_port))
        self.listen_socket.listen(10000)
        while True:
            sock, addr = self.listen_socket.accept()
            gevent.spawn(self.handle, Port(sock))

    def handle(self, port):
        while True:
            obj = port.read()
            if not obj: break
            if "_sub" in obj:
                self.broker.add_sub(obj["_sub"], port)
            else:
                self.broker.push(obj)

if __name__ == '__main__':
    from config import SERVICE_PORT
    Server().run(SERVICE_PORT)


