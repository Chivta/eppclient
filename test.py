from tests.domain_tester import DomainTester
from config import *
from tests.host_tester import HostTester


def run_all_test():

    host_test = HostTester(LOGIN, PASSWORD, CERTFILE, KEYFILE, PERMANENT_CONTACTS, PERMANENT_HOSTS, PERMANENT_DOMAINS)
    print(host_test.test_host_delete_linked_host())
    # print(tester.test_domain_create_object_exists())
    # print(tester.test_domain_create_contact_not_exists())
    # print(tester.test_domain_create_unimplemented_object_service())
    # print(tester.test_domain_create_too_many_contacts())
    # print(tester.test_domain_create_too_many_same_type_contacts())
    # print(tester.test_domain_create_same_type_same_contacts())
    # print(tester.test_domain_create_host_not_exist())
    # print(tester.test_domain_create_bad_hostAttr())
    # print(tester.test_domain_create_too_many_hosts())
    # print(tester.test_domain_create_too_big_period())

    host_test.cleanup()



def main():
    run_all_test()
    # print(tester.test_send_bad_xml())


if __name__ == "__main__":
    main()
