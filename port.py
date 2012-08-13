import struct


class Port(object):
    HEADER_STRUCT = ">L"
    HEADER_LEN = struct.calcsize(HEADER_STRUCT)

    def __init__(self, sock, f_loads=lambda x:x, f_dumps=lambda x:x):
        self._sock = sock
        self.loads = f_loads
        self.dumps = f_dumps

    def read(self):
        header = self._sock.recv(self.HEADER_LEN)
        if len(header) < self.HEADER_LEN:
            return None
        length = struct.unpack(self.HEADER_STRUCT, header)[0]
        chunks = []
        while length:
            recv = self._sock.recv(length)
            if not recv:
                return None
            chunks.append(recv)
            length -= len(recv)
        return self.loads("".join(chunks))

    def write(self, obj):
        bytes = self.dumps(obj)
        msg = struct.pack(self.HEADER_STRUCT, len(bytes)) + bytes
        self._sock.sendall(msg)

    def getvalue(self):
        return self._sock.getvalue()

    def close(self):
        self._sock.close()