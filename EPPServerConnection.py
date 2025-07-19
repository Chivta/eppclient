import socket
import ssl
import struct

# Class for handling socket, tls context and message sending/receiving
class EPPServerConnection:
    def __init__(self, host, port, certfile, keyfile):
        self.secure_sock : ssl.SSLSocket  = None
        self.sock = None
        self.context : ssl.SSLContext = None
        self.host = host
        self.port = port
        self.certfile = certfile
        self.keyfile = keyfile

        self._setup_secure_sock()

    def __del__(self):
        if self.secure_sock:
            self.secure_sock.close()
            self.secure_sock = None

    def close(self):
        if self.secure_sock:
            self.secure_sock.close()
            self.secure_sock = None

    def _setup_secure_sock(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((self.host, self.port))
        self.context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
        self.context.verify_mode = ssl.CERT_NONE
        self.context.load_cert_chain(certfile=self.certfile, keyfile=self.keyfile)


    def handshake(self):
        self.secure_sock = self.context.wrap_socket(self.sock,
                                                    server_side=False,
                                                    server_hostname=self.host,
                                                    do_handshake_on_connect=False)

        self.secure_sock.settimeout(20)
        self.secure_sock.do_handshake()

        self.read_socket()


    def send_xml(self, xml_bytes):
        if not self.secure_sock:
            raise Exception("Socket is unset")

        if not isinstance(xml_bytes, bytes):
            raise TypeError("Expected bytes, got str")

        prefix = struct.pack("!I", len(xml_bytes) + 4)
        content = prefix + xml_bytes
        self.secure_sock.sendall(content)

    def recv_exact(self, size):
        data = b""
        while len(data) < size:
            try:
                chunk = self.secure_sock.recv(size - len(data))
                if not chunk:
                    raise Exception("Connection closed by peer during recv")
                data += chunk
            except socket.timeout:
                print("timeout")
                return None
        return data

    def read_socket(self):
        if not self.secure_sock:
            raise Exception("Socket is unset")

        prefix = self.recv_exact(4)
        if prefix is None:
            raise Exception("Timed out waiting for message length")

        total_len = struct.unpack("!I", prefix)[0]

        remaining = total_len - 4
        content = self.recv_exact(remaining)

        if "</epp>" not in content.decode("utf-8"):
            raise Exception("Content didn't arrive as a whole")

        return content