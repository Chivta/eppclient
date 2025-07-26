from tkinter.messagebox import ERROR

from config import *
from EPPClient import EPPClient
from EPPServerConnection import EPPServerConnection
import XMLGenerator, MalformXMLGenerator
from EPPStream import EPPStream
from response_parsers.general_func import get_code_and_message
import tempfile
try:
    import ssl
except ImportError as er:
    raise RuntimeError(er.msg)


class Tester:
    def __init__(self, login: str, password: str, certfile: str, keyfile: str):
        self.keyfile = keyfile
        self.certfile = certfile
        self.login = login
        self.password = password

    ######### for testing if servers accepts self-created cert ########
    # def test_bad_handshake_bad_cert(self) -> tuple[bool,str]:
    #     try:
    #         if self.connection:
    #             self.connection.close()
    #         with tempfile.NamedTemporaryFile(suffix=".pem",delete_on_close=False) as bad_cert_file:
    #             with open(self.certfile,"rb") as f:
    #
    #                 ssl.
    #
    #                 content = bytearray(f.read())
    #                 if len(content) > 10:
    #                     content[10] ^= 0xFF # flip a byte at 10
    #                 bad_cert_file.write(content)
    #                 bad_cert_file.flush()
    #                 bad_cert_file.close()
    #
    #                 self.connection = EPPServerConnection(HOST,PORT,bad_cert_file.name,self.keyfile)
    #         return False,"Flipping a byte didn't cause SSLError"
    #
    #     except ssl.SSLError:
    #         return True, ""
    #     except Exception as ex:
    #         return False, f"An exception occurred: {ex}"
    #
    #     finally:
    #         if self.connection:
    #             self.connection.close()

    def test_no_login_data(self) -> tuple[bool,str]:
        try:

            connection = EPPServerConnection(HOST,PORT,self.certfile,self.keyfile)
            stream = EPPStream(self.connection)
            client = EPPClient(self.stream)

            response = client.login("","")
            code, message = get_code_and_message(response)

            if code == 2001:
                return True, ""
            else:
                return False, f"Unexpected response code: {code}, message: {message}"
        except Exception as ex:
            return False, f"An exception occurred: {ex}"


    def test_send_bad_xml(self) -> tuple[bool,str]:
        try:
            connection = EPPServerConnection(HOST,PORT,self.certfile,self.keyfile)
            stream = EPPStream(connection)
            client = EPPClient(stream)

            response = client.login(self.login,self.password)
            code, message = get_code_and_message(response)

            if code != 1000:
                return False, f"Unexpected response code: {code}, message: {message}"

            client.send_xml(MalformXMLGenerator.bad_xml())

        except ConnectionError:
            return True, ""
        except Exception as ex:
            return False, f"An exception occurred: {ex}"




def main():
    tester = Tester(LOGIN,PASSWORD,CERTFILE,KEYFILE)

    print(tester.test_send_bad_xml())



if __name__=="__main__":
    main()