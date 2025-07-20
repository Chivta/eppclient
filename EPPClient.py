import XMLGenerator
from EPPServerConnection import EPPServerConnection

# class for sending requests and getting responses
class EPPClient:
    def __init__(self, connection : EPPServerConnection):
        self.connection = connection

    def login(self, cl_id, password):
        login_xml = XMLGenerator.login(cl_id,password)
        self.connection.send_xml(login_xml)

        return self._get_response()


    def logout(self):
        logout_xml = XMLGenerator.logout()
        self.connection.send_xml(logout_xml)

        return self._get_response()

    def _get_response(self):
        response = self.connection.read_socket()
        response = response.decode("utf-8")

        return response

    def domain_check(self, domains : list[str]):
        check_domain_xml = XMLGenerator.domain_check(domains)
        self.connection.send_xml(check_domain_xml)

        return self._get_response()

    def domain_create(self, name : str, period : int, ns, registrant : str, contacts : list[(str,str)]):
        domain_create_xml = XMLGenerator.domain_create(name, period, ns, registrant, contacts)

        self.connection.send_xml(domain_create_xml)

        return self._get_response()

    def domain_info(self, domain : str):
        domain_info_xml = XMLGenerator.domain_info(domain)
        self.connection.send_xml(domain_info_xml)

        return self._get_response()

    def domain_delete(self,domain:str):
        domain_delete_xml = XMLGenerator.domain_delete(domain)
        self.connection.send_xml(domain_delete_xml)
        return self._get_response()


    def host_check(self, hosts):
        host_check_xml = XMLGenerator.host_check(hosts)
        self.connection.send_xml(host_check_xml)

        return self._get_response()

    def host_create(self,name,ipv4,ipv6):
        host_create_xml = XMLGenerator.host_create(name,ipv4,ipv6)
        self.connection.send_xml(host_create_xml)

        return self._get_response()

    def contact_info(self, contacts):
        contact_info_xml = XMLGenerator.contact_info(contacts)

        self.connection.send_xml(contact_info_xml)

        return self._get_response()

    def contact_create(self,contact_id, name, city, country_code, email, password):
        contact_create_xml = XMLGenerator.contact_create(contact_id, name, city, country_code, email, password)

        self.connection.send_xml(contact_create_xml)

        return self._get_response()

    def contact_delete(self,contact_id):
        contact_delete_xml = XMLGenerator.contact_delete(contact_id)

        self.connection.send_xml(contact_delete_xml)

        return self._get_response()