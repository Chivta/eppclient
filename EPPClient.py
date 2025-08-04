import XMLGenerator
from EPPStream import EPPStream

# class for forming and sending xml
class EPPClient:
    def __init__(self, stream: EPPStream):
        self.stream: EPPStream = stream

    def send_xml(self, xml_string):
        response = self.stream.exchange_messages(xml_string)

        return response

    def login(self, cl_id, password):
        request = XMLGenerator.login(cl_id, password)
        response = self.stream.exchange_messages(request)
        return response

    def logout(self):
        request = XMLGenerator.logout()
        response = self.stream.exchange_messages(request)
        return response

    def hello(self):
        request = XMLGenerator.hello()
        response = self.stream.exchange_messages(request)
        return response

    def domain_check(self, domains: list[str]):
        request = XMLGenerator.domain_check(domains)
        response = self.stream.exchange_messages(request)
        return response

    def domain_create(self, name: str, period: int, ns: list[str | tuple[str, dict[str:str]]], registrant: str,
                      contacts: list[tuple[str, str]]):
        request = XMLGenerator.domain_create(name, period, ns, registrant, contacts)
        response = self.stream.exchange_messages(request)
        return response

    def domain_info(self, domain: str):
        request = XMLGenerator.domain_info(domain)
        response = self.stream.exchange_messages(request)
        return response

    def domain_delete(self, domain: str):
        request = XMLGenerator.domain_delete(domain)
        response = self.stream.exchange_messages(request)
        return response

    def domain_renew(self, domain: str, cur_exp_date: str, period: int):
        request = XMLGenerator.domain_renew(domain, cur_exp_date, period)
        response = self.stream.exchange_messages(request)
        return response

    def domain_update(self, domain: str, add:dict[str:list],rem:dict[str:list],chg:dict[str:list]):
        request = XMLGenerator.domain_update(domain,add,rem,chg)
        response = self.stream.exchange_messages(request)
        return response

    def host_check(self, hosts):
        request = XMLGenerator.host_check(hosts)
        response = self.stream.exchange_messages(request)
        return response

    def host_create(self, name: str, ipv4="", ipv6=""):
        request = XMLGenerator.host_create(name, ipv4, ipv6)
        response = self.stream.exchange_messages(request)
        return response

    def host_info(self, name):
        request = XMLGenerator.host_info(name)
        response = self.stream.exchange_messages(request)
        return response

    def host_delete(self, name):
        request = XMLGenerator.host_delete(name)
        response = self.stream.exchange_messages(request)
        return response

    def contact_info(self, contacts):
        request = XMLGenerator.contact_info(contacts)
        response = self.stream.exchange_messages(request)
        return response

    def contact_create(self, contact_id, name="test", city="test", country_code="UA", email="test@test.test",
                       password="test"):
        request = XMLGenerator.contact_create(contact_id, name, city, country_code, email, password)
        response = self.stream.exchange_messages(request)
        return response

    def contact_delete(self, contact_id):
        request = XMLGenerator.contact_delete(contact_id)
        response = self.stream.exchange_messages(request)
        return response

    def contact_check(self, contact_id):
        request = XMLGenerator.contact_check(contact_id)
        response = self.stream.exchange_messages(request)
        return response
