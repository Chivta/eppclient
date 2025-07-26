import XMLGenerator
from EPPStream import EPPStream

# class for forming and sending xml
class EPPClient:
    def __init__(self, stream : EPPStream):
        self.stream: EPPStream = stream

    def send_xml(self, xml_string):
        response = self.stream.exchange_messages(xml_string)

        return response

    def login(self, cl_id, password):
        login_xml = XMLGenerator.login(cl_id,password)
        response = self.stream.exchange_messages(login_xml)

        return response

    def logout(self):
        logout_xml = XMLGenerator.logout()
        response = self.stream.exchange_messages(logout_xml)
        return response

    def hello(self):
        hello_xml = XMLGenerator.hello()
        response = self.stream.exchange_messages(hello_xml)
        return response

    def domain_check(self, domains : list[str]):
        check_domain_xml = XMLGenerator.domain_check(domains)
        response = self.stream.exchange_messages(check_domain_xml)
        return response

    def domain_create(self, name : str, period : int, ns, registrant : str, contacts : list[(str,str)]):
        domain_create_xml = XMLGenerator.domain_create(name, period, ns, registrant, contacts)

        response = self.stream.exchange_messages(domain_create_xml)
        return response

    def domain_info(self, domain : str):
        domain_info_xml = XMLGenerator.domain_info(domain)
        response = self.stream.exchange_messages(domain_info_xml)
        return response

    def domain_delete(self,domain:str):
        domain_delete_xml = XMLGenerator.domain_delete(domain)
        response = self.stream.exchange_messages(domain_delete_xml)
        return response


    def host_check(self, hosts):
        host_check_xml = XMLGenerator.host_check(hosts)
        response = self.stream.exchange_messages(host_check_xml)
        return response

    def host_create(self,name,ipv4,ipv6):
        host_create_xml = XMLGenerator.host_create(name,ipv4,ipv6)
        response = self.stream.exchange_messages(host_create_xml)
        return response

    def host_info(self,name):
        host_info_xml = XMLGenerator.host_info(name)
        response = self.stream.exchange_messages(host_info_xml)
        return response

    def contact_info(self, contacts):
        contact_info_xml = XMLGenerator.contact_info(contacts)

        response = self.stream.exchange_messages(contact_info_xml)
        return response
    def contact_create(self,contact_id, name, city, country_code, email, password):
        contact_create_xml = XMLGenerator.contact_create(contact_id, name, city, country_code, email, password)

        response = self.stream.exchange_messages(contact_create_xml)
        return response

    def contact_delete(self,contact_id):
        contact_delete_xml = XMLGenerator.contact_delete(contact_id)

        response = self.stream.exchange_messages(contact_delete_xml)

        return response