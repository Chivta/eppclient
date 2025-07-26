from EPPServerConnection import EPPServerConnection

# class for sending request and receiving responses
class EPPStream:
    def __init__(self, connection: EPPServerConnection):
        self.connection = connection

    def exchange_messages(self, request: str) -> str:
        request = request.encode("utf-8")
        self.connection.send(request)
        response = self.connection.read()
        return response.decode("utf-8")
