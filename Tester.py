from config import *
from EPPClient import EPPClient
from EPPServerConnection import EPPServerConnection
from EPPStream import EPPStream
from general_func import get_code_and_message, save_response, get_error_reason
import random
import string

try:
    import ssl
except ImportError as er:
    raise RuntimeError(er.msg)


class Tester:
    def __init__(self, login: str, password: str, certfile: str, keyfile: str, permanent_contact_id: str):
        connection = EPPServerConnection(HOST, PORT, certfile, keyfile)
        stream = EPPStream(connection)
        self.client = EPPClient(stream)

        self.client.login(login, password)

        self.temp_contact = self._create_temp_testing_contact()

        self._check_or_create_permanent_contact(permanent_contact_id)
        self.perm_contact = permanent_contact_id

    def _check_or_create_permanent_contact(self, contact_id: str):
        response = self.client.contact_check([contact_id])

        if f'<contact:id avail="0">{contact_id}</contact:id>' not in response:
            response = self.client.contact_create(contact_id, "test", "test", "UA", "test@test.test", "test")
            code, message = get_code_and_message(response)
            if code != 1000:
                raise RuntimeError(f"Could not create permanent contact ({contact_id})")

    def _create_temp_testing_contact(self):
        contact = generate_contact_name()
        response = self.client.contact_create(contact, "test", "test", "UA", "test@test.test", "test")
        code, message = get_code_and_message(response)
        for _ in range(10):
            if code == 1000:
                break
            contact = generate_contact_name()
            response = self.client.contact_create(contact, "test", "test", "UA", "test@test.test", "test")
            code, message = get_code_and_message(response)

        else:
            raise RuntimeError("Could not generate valid contact in 10 tries")

        return contact

    def cleanup(self):
        response = self.client.contact_delete(self.temp_contact)
        code, message = get_code_and_message(response)

        if code != 1000:
            raise RuntimeError(f"Could not delete test contact ({self.temp_contact}): " + message)

        response = self.client.logout()
        code, message = get_code_and_message(response)

        if code != 1500:
            raise RuntimeError(f"Could not logout:  " + message)

    def safe_create_contact(self):
        for _ in range(10):
            test_contact = generate_contact_name()
            response = self.client.contact_check(test_contact)
            if f'<contact:reason>Object exists</contact:reason>' not in response:
                break

        else:
            raise RuntimeError("Could not find non existing contact in 10 tries")

        self.client.contact_create(test_contact, "test", "test", "UA", "test@test.test", "test")

        return test_contact

    def safe_create_domain(self):
        for _ in range(10):
            temp_domain_name = generate_domain_name(suffix=".epp.ua")
            response = self.client.domain_create(temp_domain_name, 1, [], self.perm_contact, [])
            code, message = get_code_and_message(response)
            if code == 1000:
                return temp_domain_name
        raise RuntimeError("Could not create domain in 10 tries")

    def get_non_existing_contact(self):
        for _ in range(10):
            test_contact = generate_contact_name()
            response = self.client.contact_check(test_contact)
            if f'<contact:reason>Object exists</contact:reason>' not in response:
                return test_contact

        raise RuntimeError("Could not find non existing contact in 10 tries")


    def validate_code_and_reason(self, response, expected_code, expected_reason):
        reason = get_error_reason(response)

        code, message = get_code_and_message(response)

        if code == expected_code:
            if reason == expected_reason:
                return True, ""
            return False, "Expected reason: " + expected_reason + " instead got: " + reason

        return False, message

    def test_domain_create_invalid_name(self) -> tuple[bool, str]:
        expected_code = 2005
        expected_reason = "Incorrect domain name"

        try:
            domain_name = generate_domain_name(suffix=".com")

            response = self.client.domain_create(domain_name, 1, [], self.temp_contact, [])
            result, message = self.validate_code_and_reason(response, expected_code, expected_reason)

            if not result:
                self.client.domain_delete(domain_name)
            return result, message

        except Exception as ex:
            return False, f"An exception occurred: {ex}"

    def test_domain_create_object_exists(self) -> tuple[bool, str]:
        expected_code = 2302
        expected_reason = "Object exists"

        try:
            temp_domain_name = self.safe_create_domain()

            # creating same domain again
            response = self.client.domain_create(temp_domain_name, 1, [], self.perm_contact, [])

            result, message = self.validate_code_and_reason(response, expected_code, expected_reason)

            response = self.client.domain_delete(temp_domain_name)
            temp_domain_deletion_code, _ = get_code_and_message(response)

            if temp_domain_deletion_code not in (1000, 1001):
                raise RuntimeError("Could not delete temp domain")

            return result, message

        except Exception as ex:
            return False, f"An exception occurred: {ex}"

    def test_domain_create_unimplemented_object_service(self):
        expected_code = 2307
        expected_reason = "You do not have access to registration in this public domain"


        try:
            domain_name = generate_domain_name(suffix=".ua")

            response = self.client.domain_create(domain_name, 1, [], self.temp_contact, [])

            result, message = self.validate_code_and_reason(response, expected_code, expected_reason)

            if not result:
                self.client.domain_delete(domain_name)

            return result, message


        except Exception as ex:
            return False, f"An exception occurred: {ex}"


    def test_domain_create_command_syntax_error(self):
        expected_code = 2001
        expected_reason = "Element '{http://hostmaster.ua/epp/domain-1.1}registrant': [facet 'minLength'] The value has a length of '0'; this underruns the allowed minimum length of '3'."

        try:
            domain_name = generate_domain_name()

            response = self.client.domain_create(domain_name, 1, [], "", [])

            result, message = self.validate_code_and_reason(response, expected_code, expected_reason)

            if not result:
                self.client.domain_delete(domain_name)

            return result, message

        except Exception as ex:
            return False, f"An exception occurred: {ex}"

    def test_domain_create_object_not_exists(self):
        expected_code = 2303
        expected_reason = "incorrect element registrant"


        try:
            domain_name = generate_domain_name()

            test_contact = self.get_non_existing_contact()

            response = self.client.domain_create(domain_name, 1, [], test_contact, [])
            result, message = self.validate_code_and_reason(response, expected_code, expected_reason)

            if not result:
                self.client.domain_delete(domain_name)

            return result, message

        except Exception as ex:
            return False, f"An exception occurred: {ex}"

    def test_domain_create_too_many_contacts(self):
        expected_code = 2001
        expected_reason = ""

        try:

            # creating temp contacts
            contact_list = [self.safe_create_contact() for _ in range(6)]

            domain_name = generate_domain_name()

            response = self.client.domain_create(domain_name, 1, [], self.perm_contact,
                                                 [("admin", contact) for contact in contact_list] +
                                                 [("tech", contact) for contact in contact_list] +
                                                 [("billing", contact) for contact in contact_list])

            result, message = self.validate_code_and_reason(response, expected_code, expected_reason)

            if not result:
                self.client.domain_delete(domain_name)

            # Always try to delete contacts, even if deletion might fail
            for contact in contact_list:
                response = self.client.contact_delete(contact)
                code = get_code_and_message(response)[0]
                if code not in (1000, 1001, 2304):  # 2304 = Object not found
                    raise RuntimeError(f"Could not delete contact ({contact}), code: {code}")

            return result, message

        except Exception as ex:
            return False, f"An exception occurred: {ex}"


def generate_domain_name(suffix=".epp.ua"):
    return "".join(random.choice(string.ascii_lowercase) for _ in range(10)) + suffix


def generate_contact_name():
    return "".join(random.choice(string.ascii_lowercase) for _ in range(6))


def run_all_test():
    tester = Tester(LOGIN, PASSWORD, CERTFILE, KEYFILE, PERMANENT_CONTACT_ID)
    print(tester.test_domain_create_invalid_name())
    print(tester.test_domain_create_command_syntax_error())
    print(tester.test_domain_create_object_exists())
    print(tester.test_domain_create_object_not_exists())
    print(tester.test_domain_create_unimplemented_object_service())
    print(tester.test_domain_create_too_many_contacts())
    # tester.cleanup()


def main():
    run_all_test()
    # print(tester.test_send_bad_xml())


if __name__ == "__main__":
    main()
