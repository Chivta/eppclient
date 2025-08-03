from config import *
from EPPClient import EPPClient
from EPPServerConnection import EPPServerConnection
from EPPStream import EPPStream
from general_func import get_code_and_message, get_error_reason, get_code
import random
import string

try:
    import ssl
except ImportError as er:
    raise RuntimeError(er.msg)

# decorator for printing test name
def test_with_name(name):
    def decorator(fn):
        def wrapper(self, *args, **kwargs):
            print(f"Test name: {name}")
            return fn(self, *args, **kwargs)

        return wrapper

    return decorator

# decorator for validating response received from test function
def expect(expected_code: int, expected_reason: str = ""):
    def decorator(func):
        def wrapper(self, *args, **kwargs) -> (bool, str):
            try:
                response = func(self, *args, **kwargs)
                code, msg = get_code_and_message(response)
                reason = get_error_reason(response)

                if expected_code == code:
                    if expected_reason == reason:
                        return True, ""
                    return False, f'Correct code: {expected_code}. Expected reason: "{expected_reason}", but got reason: "{reason}". Message: "{msg}"'
                return False, f'Expected code: {expected_code}, but got: {code}. Expected reason: "{expected_reason}", got: "{reason}". Message: "{msg}"'

            except Exception as ex:
                return False, f"An error occurred: {ex}"

        return wrapper

    return decorator


class Tester:
    def __init__(self, login: str, password: str, certfile: str, keyfile: str, permanent_contacts: list, permanent_hosts: list):
        connection = EPPServerConnection(HOST, PORT, certfile, keyfile)
        stream = EPPStream(connection)
        self.client = EPPClient(stream)

        self.client.login(login, password)

        self._check_or_create_permanent_contacts(permanent_contacts)
        self.perm_contacts: list = permanent_contacts

        self._check_or_create_permanent_hosts(permanent_hosts)
        self.perm_hosts = permanent_hosts

        self.domains_to_delete = []
        self.contacts_to_delete = []
        self.hosts_to_delete = []

    def _check_or_create_permanent_hosts(self,hosts: list):
        for host in hosts:
            response = self.client.host_check([host])

            if f'<host:name avail="0">{host}</host:name>' not in response:
                response = self.client.domain_check(host)
                if f'<domain:name avail="0">{host}</domain:name>' not in response:
                    response = self.client.domain_create(host,1,[],self.perm_contacts[0],[])
                    if get_code(response) !=1000:
                        raise RuntimeError('Could not create domain for host "{host}"')

                response = self.client.host_create(host, "1.1.1.1")
                code, message = get_code_and_message(response)
                if code != 1000:
                    raise RuntimeError(f'Could not create permanent host "{host}"')

    def _check_or_create_permanent_contacts(self, contacts: list):
        for contact_id in contacts:
            response = self.client.contact_check([contact_id])

            if f'<contact:id avail="0">{contact_id}</contact:id>' not in response:
                response = self.client.contact_create(contact_id, "test", "test", "UA", "test@test.test", "test")
                code, message = get_code_and_message(response)
                if code != 1000:
                    raise RuntimeError(f"Could not create permanent contact ({contact_id})")


    def cleanup(self):
        for domain in self.domains_to_delete:
            self.client.domain_delete(domain)
        self.domains_to_delete.clear()

        for contact in self.contacts_to_delete:
            self.client.contact_delete(contact)
        self.contacts_to_delete.clear()

        for host in self.hosts_to_delete:
            self.client.host_delete(host)
        self.hosts_to_delete.clear()

        response = self.client.logout()
        code, message = get_code_and_message(response)

        if code != 1500:
            raise RuntimeError(f"Could not logout:  " + message)

    def safe_create_contact(self):
        name = self.get_non_existing_contact()
        response = self.client.contact_create(name)
        if get_code(response) != 1000:
            raise RuntimeError(f'Could not create "{name}" contact')
        return name


    def safe_create_host(self, suffix=".epp.ua"):
        name = self.get_non_existing_domain(suffix)
        response = self.client.domain_create(name,1,[],self.perm_contacts[0],[])
        if get_code(response) != 1000:
            raise RuntimeError(f'Could not create "{name}" domain')

        response = self.client.host_create(name,"1.1.1.1")
        if get_code(response) != 1000:
            raise RuntimeError(f'Could not create "{name}" host')
        return name


    def get_non_existing_contact(self):
        return try_until_success(
            generate_random_name,
            lambda name: f'<contact:reason>Object exists</contact:reason>' not in self.client.contact_check(name),
            length=10)

    def get_non_existing_host(self, suffix=".epp.ua"):
        return try_until_success(
            generate_random_name,
            lambda name: f'<host:reason>Object exists</host:reason>' not in self.client.host_check(name),
            length=10,suffix=suffix)

    def get_non_existing_domain(self, suffix=".epp.ua"):
        return try_until_success(
            generate_random_name,
            lambda name: f'<domain:reason>Object exists</domain:reason>' not in self.client.domain_check(name),
            length=10, suffix=suffix)

    @test_with_name("test_domain_create_invalid_name")
    @expect(2005, "Incorrect domain name")
    def test_domain_create_invalid_name(self) -> tuple[bool, str]:
        domain_name = generate_random_name(10, suffix=".com")

        response = self.client.domain_create(domain_name, 1, [], self.perm_contacts[0], [])

        self.domains_to_delete.append(domain_name)

        return response

    @test_with_name("test_domain_create_object_exists")
    @expect(2302, "Object exists")
    def test_domain_create_object_exists(self) -> tuple[bool, str]:
        temp_domain_name = self.get_non_existing_domain()
        self.client.domain_create(temp_domain_name,1,[],self.perm_contacts[0],[])
        self.domains_to_delete.append(temp_domain_name)

        # creating same domain again
        response = self.client.domain_create(temp_domain_name, 1, [], self.perm_contacts[0], [])

        return response

    @test_with_name("test_domain_create_unimplemented_object_service")
    @expect(2307, "You do not have access to registration in this public domain")
    def test_domain_create_unimplemented_object_service(self):
        domain_name = generate_random_name(10, suffix=".ua")

        response = self.client.domain_create(domain_name, 1, [], self.perm_contacts[0], [])

        self.domains_to_delete.append(domain_name)

        return response

    @test_with_name("test_domain_create_no_registrant")
    @expect(2001,
            "Element '{http://hostmaster.ua/epp/domain-1.1}registrant': [facet 'minLength'] The value has a length of '0'; this underruns the allowed minimum length of '3'.")
    def test_domain_create_no_registrant(self):
        domain_name = generate_random_name(10, suffix=".epp.ua")

        response = self.client.domain_create(domain_name, 1, [], "", [])

        self.domains_to_delete.append(domain_name)

        return response

    @test_with_name("test_domain_create_contact_not_exists")
    @expect(2303, "incorrect element registrant")
    def test_domain_create_contact_not_exists(self):
        domain_name = generate_random_name(10, suffix=".epp.ua")

        test_contact = try_until_success(self.get_non_existing_contact, lambda name: name is not None)

        response = self.client.domain_create(domain_name, 1, [], test_contact, [])

        self.domains_to_delete.append(domain_name)

        return response

    @test_with_name("test_domain_create_too_many_contacts")
    @expect(2001,
            "Element \'{http://hostmaster.ua/epp/domain-1.1}contact\': This element is not expected. Expected is ( {http://hostmaster.ua/epp/domain-1.1}authInfo ).")
    def test_domain_create_too_many_contacts(self):
        # creating temp contacts
        contact_list = [self.safe_create_contact() for _ in range(6)]

        domain_name = generate_random_name(10, suffix=".epp.ua")

        response = self.client.domain_create(domain_name, 1, [], self.perm_contacts[0],
                                             [("admin", contact) for contact in contact_list] +
                                             [("tech", contact) for contact in contact_list] +
                                             [("billing", contact) for contact in contact_list])

        self.domains_to_delete.append(domain_name)

        self.contacts_to_delete.extend(contact_list)

        return response

    @test_with_name("test_domain_create_too_many_same_type_contacts")
    @expect(2001, "Contacts limit exceeded: admin")
    def test_domain_create_too_many_same_type_contacts(self):
        # creating temp contacts
        contact_list = [self.safe_create_contact() for _ in range(9)]

        domain_name = generate_random_name(10, suffix=".epp.ua")

        response = self.client.domain_create(domain_name, 1, [], self.perm_contacts[0],
                                             [("admin", contact) for contact in contact_list])

        self.domains_to_delete.append(domain_name)

        self.contacts_to_delete.extend(contact_list)

        return response

    @test_with_name("test_domain_create_same_type_same_contacts")
    @expect(2005, "Field duplicates domain:contact")
    def test_domain_create_same_type_same_contacts(self):
        domain_name = generate_random_name(10, suffix=".epp.ua")

        response = self.client.domain_create(domain_name, 1, [], self.perm_contacts[0],
                                             [("admin", self.perm_contacts[0]), ("admin", self.perm_contacts[0])])

        self.domains_to_delete.append(domain_name)

        return response

    @test_with_name("test_domain_create_host_not_exist")
    @expect(2303, "incorrect element domain:hostObj")
    def test_domain_create_host_not_exist(self):
        domain_name = generate_random_name(10, suffix=".epp.ua")

        non_existing_host = self.get_non_existing_host()

        response = self.client.domain_create(domain_name, 1, [non_existing_host], self.perm_contacts[0], [])

        self.domains_to_delete.append(domain_name)

        return response

    @test_with_name("test_domain_create_bad_hostAttr")
    @expect(2005, "incorrect element domain:hostObj")
    def test_domain_create_bad_hostAttr(self):
        domain_name = generate_random_name(10, suffix=".epp.ua")

        invalid_host_name = "2sd@!!"
        response = self.client.domain_create(domain_name, 1, [invalid_host_name], self.perm_contacts[0], [])

        self.domains_to_delete.append(domain_name)

        return response

    # @test_name("test_domain_create_same_hosts")
    # @expect(2005, "")
    # def test_domain_create_same_hosts(self):
    #     # host_name = self.safe_create_host()
    #     domain_name=self.get_non_existing_domain()
    #     self.client.domain_create(domain_name,1,[],self.perm_contacts[0],[])
    #     response = self.client.domain_create("mx1."+domain_name, 1, [(domain_name,{"v4":"1.2.1.1"})], self.perm_contacts[0], [])
    #
    #     # self.domains_to_delete.append(domain_name)
    #
    #     return response

    @test_with_name("test_domain_create_too_many_hosts")
    @expect(2001, "Element \'{http://hostmaster.ua/epp/domain-1.1}hostObj\': This element is not expected.")
    def test_domain_create_too_many_hosts(self):
        domain_name=self.get_non_existing_domain()

        response = self.client.domain_create(domain_name, 1, [host for host in self.perm_hosts], self.perm_contacts[0], [])

        self.domains_to_delete.append(domain_name)

        return response

    @test_with_name("test_domain_create_too_many_hosts")
    @expect(2004, "Period exceeded the maximum value")
    def test_domain_create_too_big_period(self):
        domain_name=self.get_non_existing_domain()

        response = self.client.domain_create(domain_name, 12, [], self.perm_contacts[0], [])

        self.domains_to_delete.append(domain_name)

        return response

def generate_random_name(length, suffix=""):
    return "".join(random.choice(string.ascii_lowercase) for _ in range(length)) + suffix


def try_until_success(create_func, check_success, tries=10, *args, **kwargs):
    for _ in range(tries):
        item = create_func(*args, **kwargs)
        if check_success(item):
            return item
    raise RuntimeError("Max retries reached")


def run_all_test():
    tester = Tester(LOGIN, PASSWORD, CERTFILE, KEYFILE, PERMANENT_CONTACTS, PERMANENT_HOSTS)
    print(tester.test_domain_create_invalid_name())
    print(tester.test_domain_create_no_registrant())
    print(tester.test_domain_create_object_exists())
    print(tester.test_domain_create_contact_not_exists())
    print(tester.test_domain_create_unimplemented_object_service())
    print(tester.test_domain_create_too_many_contacts())
    print(tester.test_domain_create_too_many_same_type_contacts())
    print(tester.test_domain_create_same_type_same_contacts())
    print(tester.test_domain_create_host_not_exist())
    print(tester.test_domain_create_bad_hostAttr())
    print(tester.test_domain_create_too_many_hosts())
    print(tester.test_domain_create_too_big_period())
    tester.cleanup()


def main():
    run_all_test()
    # print(tester.test_send_bad_xml())


if __name__ == "__main__":
    main()
