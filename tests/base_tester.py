from config import *
from EPPClient import EPPClient
from EPPServerConnection import EPPServerConnection
from EPPStream import EPPStream
from general_func import get_code_and_message, get_error_reason, get_code, save_response
import random
import string

try:
    import ssl
except ImportError as er:
    raise RuntimeError(er.msg)

def generate_random_name(length, suffix=""):
    return "".join(random.choice(string.ascii_lowercase) for _ in range(length)) + suffix


def try_until_success(create_func, check_success, tries=10, *args, **kwargs):
    for _ in range(tries):
        item = create_func(*args, **kwargs)
        if check_success(item):
            return item
    raise RuntimeError("Max retries reached")

# decorator for printing test name
def test_with_name(name):
    def decorator(fn):
        def wrapper(self, *args, **kwargs):
            print(f"▶ Test name: {name} ", end="")
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

class TestContext:
    def __init__(self, login: str, password: str, certfile: str, keyfile: str, permanent_contacts: list,
                 permanent_hosts: list, permanent_domains: list):
        connection = EPPServerConnection(HOST, PORT, certfile, keyfile)
        stream = EPPStream(connection)
        self.client = EPPClient(stream)

        self.client.login(login, password)

        self._check_or_create_contacts(permanent_contacts)
        self.perm_contacts: list = permanent_contacts

        self._check_or_create_domains(permanent_domains)
        self.perm_domains: list = permanent_domains

        self._check_or_create_hosts(permanent_hosts)
        self.perm_hosts: list = permanent_hosts

        self.domains_to_delete = []
        self.contacts_to_delete = []
        self.hosts_to_delete = []


    def _check_or_create_domains(self, domains: list):
        for domain in domains:
            response = self.client.domain_check([domain])

            if f'<domain:name avail="0">{domain}</domain:name>' not in response:
                response = self.client.domain_create(domain, 1,[],self.perm_contacts[0],[])
                code, message = get_code_and_message(response)
                if code != 1000:
                    raise RuntimeError(f'Could not create domain "{domain}"')

    def _check_or_create_hosts(self, hosts: list):
        for host in hosts:
            response = self.client.host_check([host])

            if f'<host:name avail="0">{host}</host:name>' not in response:
                response = self.client.host_create(host, "1.1.1.1")
                code, message = get_code_and_message(response)
                if code != 1000:
                    raise RuntimeError(f'Could not create host "{host}"')

    def _check_or_create_contacts(self, contacts: list):
        for contact_id in contacts:
            response = self.client.contact_check([contact_id])

            if f'<contact:id avail="0">{contact_id}</contact:id>' not in response:
                response = self.client.contact_create(contact_id, "test", "test", "UA", "test@test.test", "test")
                code, message = get_code_and_message(response)
                if code != 1000:
                    raise RuntimeError(f"Could not create contact ({contact_id})")

    def cleanup(self):
        for host in self.hosts_to_delete:
            self.client.host_delete(host)
        self.hosts_to_delete.clear()

        for domain in self.domains_to_delete:
            self.client.domain_delete(domain)
        self.domains_to_delete.clear()

        for contact in self.contacts_to_delete:
            self.client.contact_delete(contact)
        self.contacts_to_delete.clear()

        response = self.client.logout()
        code, message = get_code_and_message(response)

        if code != 1500:
            raise RuntimeError(f"Could not logout:  " + message)


class Tester:
    def __init__(self, context: TestContext):
        self.client = context.client

        self.perm_contacts: list = context.perm_contacts

        self.perm_domains: list = context.perm_domains

        self.perm_hosts: list = context.perm_hosts

        self.domains_to_delete = context.domains_to_delete
        self.contacts_to_delete = context.contacts_to_delete
        self.hosts_to_delete = context.hosts_to_delete

    def safe_create_contact(self):
        name = self.get_available_contact_name()
        response = self.client.contact_create(name)
        if get_code(response) != 1000:
            raise RuntimeError(f'Could not create "{name}" contact')
        return name

    def safe_create_host(self, suffix=".epp.ua") -> str:
        name = self.get_available_host_name(suffix)

        response = self.client.host_create(name)
        save_response(response)
        if get_code(response) != 1000:
            raise RuntimeError(f'Could not create "{name}" host')
        return name

    def get_available_contact_name(self):
        return try_until_success(
            generate_random_name,
            lambda name: f'<contact:reason>Object exists</contact:reason>' not in self.client.contact_check(name),
            length=10)

    def get_available_host_name(self, suffix=".epp.ua"):
        return try_until_success(
            generate_random_name,
            lambda name: f'<host:reason>Object exists</host:reason>' not in self.client.host_check(name),
            length=10, suffix=suffix)

    def get_available_domain_name(self, suffix=".epp.ua", length=10):
        return try_until_success(
            generate_random_name,
            lambda name: f'<domain:reason>Object exists</domain:reason>' not in self.client.domain_check(name),
            length=length, suffix=suffix)