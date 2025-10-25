from tests.contact_tester import ContactTester
from tests.domain_tester import DomainTester
from tests.host_tester import HostTester
from tests.base_tester import TestContext
from ssl import SSLError
from config import *

if LOGIN == "":
    print("ERR: Login in config.py is empty")
    exit(1)
if PASSWORD == "":
    print("ERR: Password in config.py is empty")
    exit(1)
    
print("Creating testing context...")

try:
    context = TestContext(LOGIN, PASSWORD, CERTFILE, KEYFILE)
except FileNotFoundError:
    print("ERR: Files {CERTFILE} and {KEYFILE} were not found")
    exit(1)
except SSLError:
    print("ERR: Bad cert or key")
    exit(1)
except ConnectionError:
    print("ERR: Connection closed unexpectedly")
    exit(1)


domain_test = DomainTester(context)
host_test = HostTester(context)
contact_test = ContactTester(context)

TESTS = {

}

TESTS['contact'] = [
    ('Contact check with too many hosts', contact_test.check_too_many_contacts),
    ('Contact info with syntax error', contact_test.info_syntax_error),
    ('Contact info with value syntax error', contact_test.info_value_syntax_error),
    ('Contact info with unexisting contact', contact_test.info_unexisting_contact),
    ('Contact create with syntax error', contact_test.create_syntax_error),
    ('Contact create with value syntax error', contact_test.create_value_syntax_error),
    # ('Contact create required parameter missing', contact_test.create_required_parameter_missing),  # commented out in your code
    ('Contact create with existing object', contact_test.create_object_exists),
    ('Contact delete with syntax error', contact_test.delete_syntax_error),
    ('Contact delete with value syntax error', contact_test.delete_value_syntax_error),
    ('Contact delete with unexisting contact', contact_test.delete_object_not_exists),
    ('Contact delete on contact with status clientDeleteProhibited', contact_test.delete_status_prohibits_operation),
    ('Contact delete on contact linked to a domain', contact_test.delete_object_association_prohibits),
    ('Contact update with syntax error', contact_test.update_syntax_error),
    ('Contact update with value syntax error', contact_test.update_value_syntax_error),
    ('Contact update with unexisting contact', contact_test.update_unexisting_contact),
    ('Contact update on contact with status updateProhibited', contact_test.update_status_prohibits_operation),
]

TESTS['host'] = [
    ("Host check with too many hosts", host_test.check_too_many_hosts),
    ("Host info with syntax error", host_test.info_syntax_error),
    ("Host info with value syntax error", host_test.info_value_syntax_error),
    ("Host info of unexisting host", host_test.info_unexisting_host),
    ("Host create with syntax error", host_test.create_syntax_error),
    ("Host create with value syntax error", host_test.create_value_syntax_error),
    ("Host create without ips", host_test.create_no_ip),
    ("Host create with incorrect ip", host_test.create_incorrect_ip),
    ("Host create with existing host", host_test.create_existing_host),
    ("Host create without parent domain", host_test.create_no_parent_domain),
    ("Host create bad external host", host_test.create_bad_external_host),
    ("Host delete with syntax error", host_test.delete_syntax_error),
    ("Host delete with value syntax error", host_test.delete_value_syntax_error),
    ("Host delete on host with clientDeleteProhibited status", host_test.delete_status_prohibits_operation),
    ("Host delete on unexisting host", host_test.delete_linked_host),
    ("Host update with syntax error", host_test.update_syntax_error),
    ("Host update with value syntax error", host_test.update_value_syntax_error),
    ("Host update with unexisting host", host_test.update_unexisting_host),
    ("Host update status prohibits operation", host_test.update_status_prohibits_operation),
]

TESTS['domain'] = [
    ("Domain create .com domain", domain_test.create_invalid_name),
    ("Domain create existing domain", domain_test.create_object_exists),
    ("Domain create .ua domain", domain_test.create_unimplemented_object_service),
    ("Domain create without registrant element", domain_test.create_no_registrant),
    ("Domain create with unexisting contact", domain_test.create_contact_not_exists),
    ("Domain create with >16 total contacts", domain_test.create_too_many_contacts),
    ("Domain create with >8 contacts of the same type", domain_test.create_too_many_same_type_contacts),
    ("Domain create with reoccurring contact of the same type", domain_test.create_same_type_same_contacts),
    ("Domain create with unexisting host object", domain_test.create_host_not_exist),
    ("Domain create with host attributes with unsupported name", domain_test.create_bad_hostAttr),
    ("Domain create with >13 hosts", domain_test.create_too_many_hosts),
    ("Domain create with too big period", domain_test.create_too_big_period),
    ("Domain check with too many domains", domain_test.check_too_many_domains),
    ("Domain info with .com domain", domain_test.info_incorrect_domain_name),
    ("Domain info with unexisting domain", domain_test.info_unexisting_domain),
    ("Domain delete with .com domain", domain_test.delete_incorrect_domain_name),
    ("Domain delete with unexisting domain", domain_test.delete_non_existing_domain),
    ("Domain delete on domain with redemptionPeriod status", domain_test.delete_status_prohibits_operation),
    ("Domain delete on domain that's associated to host", domain_test.delete_association_prohibits_operation),
    ("Domain renew with too long period", domain_test.renew_too_long_result_period),
    ("Domain renew with syntax error", domain_test.renew_syntax_error),
    ("Domain renew with value syntax error", domain_test.renew_value_syntax_error),
    ("Domain renew with wrong expire date", domain_test.renew_wrong_expire_date),
    ("Domain renew with unexisting domain", domain_test.renew_unexisting_domain),
    ("Domain renew on domain with redemptionPeriod status", domain_test.renew_deleted_domain),
    ("Domain update with value syntax error", domain_test.update_syntax_error),
    ("Domain update with value syntax error", domain_test.update_value_syntax_error),
    ("Domain update with unexisting domain", domain_test.update_unexisting_domain),
    ("Domain update on domain with redemptionPeriod status", domain_test.update_deleted_domain),
    ("Domain restore with value syntax error", domain_test.restore_syntax_error),
    ("Domain restore with value syntax error", domain_test.restore_value_syntax_error),
    ("Domain restore with unexisting domain", domain_test.restore_unexisting_domain),
    ("Domain restore on domain without redemptionPeriod status", domain_test.restore_not_deleted_domain),
    ("Domain restore with now empty change block", domain_test.restore_with_chg_block),
]

def run_tests_console():
    while True:
        print("\n=== MAIN MENU ===")
        print("0. Run ALL tests")
        for idx, key in enumerate(TESTS.keys(), 1):
            print(f"{idx}. {key.capitalize()}")
        print("4. Quit")

        choice = input("Choose an option: ").strip()
        if choice == '4':
            break

        if choice == '0':
            run_all_tests()
            continue

        try:
            category = list(TESTS.keys())[int(choice) - 1]
        except (ValueError, IndexError):
            print("Invalid choice.")
            continue

        run_category_menu(category)

def run_test(func):
    res, info = func()
    if res:
        print("PASSED")
    if not res:
        print("NOT PASSED " + info)

def run_all_tests():
    for category, tests in TESTS.items():
        print(f"\n-- Running all {category} tests --")
        for name, func in tests:
            run_test(func)



def run_category_menu(category):
    tests = TESTS[category]

    while True:
        print(f"\n=== {category.upper()} TESTS ===")
        print("0. Run all in this category")
        for idx, (name, _) in enumerate(tests, 1):
            print(f"{idx}. {name}")
        print("b. Back")

        choice = input("Choose a test to run: ").strip()
        if choice == 'b':
            break

        if choice == '0':
            for name, func in tests:
                run_test(func)
            continue

        try:
            name, func = tests[int(choice) - 1]
        except (ValueError, IndexError):
            print("Invalid choice.")
            continue

        run_test(func)


def main():
    try:
        run_tests_console()
    except KeyboardInterrupt:
        pass
    finally:
        print("\nRunning cleanup and exiting...")
        context.cleanup()


if __name__ == "__main__":
    main()
