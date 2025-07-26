from config import *
from EPPClient import EPPClient
from EPPServerConnection import EPPServerConnection
import XMLGenerator, MalformXMLGenerator
from EPPStream import EPPStream
from response_parsers.general_func import get_code_and_message


class Tester:
    def __init__(self, login: str, password: str, certfile: str, keyfile: str):
        self.stream: EPPStream = None
        self.client: EPPClient = None
        self.connection: EPPServerConnection = None
        self.keyfile = keyfile
        self.certfile = certfile
        self.login = login
        self.password = password

    def test_bad_handshake_malformed_login(self) -> tuple[bool,str]:
        try:
            if self.connection:
                self.connection.close()

            self.connection = EPPServerConnection(HOST,PORT,self.certfile,self.keyfile)
            self.stream = EPPStream(self.connection)
            self.client = EPPClient(self.stream)

            response = self.client.login("","")
            code, message = get_code_and_message(response)

            if code == 2001:
                return True,""
            else:
                return False, f"Unexpected response code: {code}, message: {message}"
        except Exception as ex:
            return False, f"An exception occured: {ex}"








def main():
    tester = Tester("","",CERTFILE,KEYFILE)

    print(tester.test_bad_handshake_malformed_login())



if __name__=="__main__":
    main()