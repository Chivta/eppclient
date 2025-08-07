from MalformXMLGenerator import domain_create_no_registrant, domain_update_without_domain_name, \
    domain_restore_without_domain_name, domain_restore_with_change_block
from general_func import get_code_and_message, get_error_reason, get_code, save_response, get_exp_date
from tests.base_tester import Tester, test_with_name, expect, generate_random_name


class DomainTester(Tester):
    @test_with_name("Creating .com domain")
    @expect(2005, "Incorrect domain name")
    def test_domain_create_invalid_name(self) -> tuple[bool, str]:
        domain_name = self.get_available_domain_name(suffix=".com")

        response = self.client.domain_create(domain_name, 1, [], self.perm_contacts[0], [])

        self.domains_to_delete.append(domain_name)

        return response

    @test_with_name("Creating existing domain")
    @expect(2302, "Object exists")
    def test_domain_create_object_exists(self) -> tuple[bool, str]:
        temp_domain_name = self.get_available_domain_name()
        self.client.domain_create(temp_domain_name, 1, [], self.perm_contacts[0], [])
        self.domains_to_delete.append(temp_domain_name)

        # creating same domain again
        response = self.client.domain_create(temp_domain_name, 1, [], self.perm_contacts[0], [])

        return response

    @test_with_name("Creating .ua domain")
    @expect(2307, "You do not have access to registration in this public domain")
    def test_domain_create_unimplemented_object_service(self):
        domain_name = self.get_available_domain_name(suffix=".ua")

        response = self.client.domain_create(domain_name, 1, [], self.perm_contacts[0], [])

        self.domains_to_delete.append(domain_name)

        return response

    @test_with_name("Domain create without registrant element")
    @expect(2001,
            "Element \'{http://hostmaster.ua/epp/domain-1.1}create\': Missing child element(s). Expected is one of ( {http://hostmaster.ua/epp/domain-1.1}ns, {http://hostmaster.ua/epp/domain-1.1}registrant ).")
    def test_domain_create_no_registrant(self):
        domain_name = self.get_available_domain_name()

        response = self.client.send_xml(domain_create_no_registrant(domain_name, 1, [], []))

        self.domains_to_delete.append(domain_name)

        return response

    @test_with_name("Domain create with unexisting contact")
    @expect(2303, "incorrect element registrant")
    def test_domain_create_contact_not_exists(self):
        domain_name = self.get_available_domain_name()

        test_contact = self.get_available_contact_name()

        response = self.client.domain_create(domain_name, 1, [], test_contact, [])

        self.domains_to_delete.append(domain_name)

        return response

    @test_with_name("Domain create with >16 total contacts")
    @expect(2001,
            "Element \'{http://hostmaster.ua/epp/domain-1.1}contact\': This element is not expected. Expected is ( {http://hostmaster.ua/epp/domain-1.1}authInfo ).")
    def test_domain_create_too_many_contacts(self):
        domain_name = self.get_available_domain_name()

        response = self.client.domain_create(domain_name, 1, [], self.perm_contacts[0],
                                             [("admin", generate_random_name(10)) for _ in range(17)])

        self.domains_to_delete.append(domain_name)

        return response

    @test_with_name("Domain create with >8 contacts of the same type")
    @expect(2001, "Contacts limit exceeded: admin")
    def test_domain_create_too_many_same_type_contacts(self):
        domain_name = self.get_available_domain_name()

        response = self.client.domain_create(domain_name, 1, [], self.perm_contacts[0],
                                             [("admin", contact) for contact in self.perm_contacts])

        self.domains_to_delete.append(domain_name)

        return response

    @test_with_name("Domain create with reoccurring contact of the same type")
    @expect(2005, "Field duplicates domain:contact")
    def test_domain_create_same_type_same_contacts(self):
        domain_name = self.get_available_domain_name()

        response = self.client.domain_create(domain_name, 1, [], self.perm_contacts[0],
                                             [("admin", self.perm_contacts[0]), ("admin", self.perm_contacts[0])])

        self.domains_to_delete.append(domain_name)

        return response

    @test_with_name("Domain create with unexisting host object")
    @expect(2303, "incorrect element domain:hostObj")
    def test_domain_create_host_not_exist(self):
        domain_name = self.get_available_domain_name()

        non_existing_host = self.get_available_host_name()

        response = self.client.domain_create(domain_name, 1, [non_existing_host], self.perm_contacts[0], [])

        self.domains_to_delete.append(domain_name)

        return response

    @test_with_name("Domain create with host attributes with unsupported name")
    @expect(2005, "incorrect element domain:hostObj")
    def test_domain_create_bad_hostAttr(self):
        domain_name = self.get_available_domain_name()

        invalid_host_name = "2sd@!!"
        response = self.client.domain_create(domain_name, 1, [invalid_host_name], self.perm_contacts[0], [])

        self.domains_to_delete.append(domain_name)

        return response

    @test_with_name("Domain create with >13 hosts")
    @expect(2001, "Element \'{http://hostmaster.ua/epp/domain-1.1}hostObj\': This element is not expected.")
    def test_domain_create_too_many_hosts(self):
        domain_name = self.get_available_domain_name()

        response = self.client.domain_create(domain_name, 1, [generate_random_name(10, ".epp.ua") for _ in range(14)],
                                             self.perm_contacts[0], [])

        self.domains_to_delete.append(domain_name)

        return response

    @test_with_name("Domain create with too big period")
    @expect(2004, "Period exceeded the maximum value")
    def test_domain_create_too_big_period(self):
        domain_name = self.get_available_domain_name()

        response = self.client.domain_create(domain_name, 100, [], self.perm_contacts[0], [])

        self.domains_to_delete.append(domain_name)

        return response

    @test_with_name("Domain check with too many domains")
    @expect(2001, "Element \'{http://hostmaster.ua/epp/domain-1.1}name\': This element is not expected.")
    def test_domain_check_too_many_domains(self):
        domain_names = [self.get_available_domain_name() for _ in range(11)]

        response = self.client.domain_check(domain_names)

        return response @ test_with_name("test_domain_check_too_many_domains")

    @test_with_name("Domain info with .com domain")
    @expect(2005, "Incorrect domain name")
    def test_domain_info_incorrect_domain_name(self):
        domain_name = self.get_available_domain_name(suffix=".com")

        response = self.client.domain_info(domain_name)

        return response

    @test_with_name("Domain info with unexisting domain")
    @expect(2303, "Object does not exist")
    def test_domain_info_unexisting_domain(self):
        domain_name = self.get_available_domain_name()

        response = self.client.domain_info(domain_name)

        return response

    @test_with_name("Domain delete with .com domain")
    @expect(2005, "Incorrect domain name")
    def test_domain_delete_incorrect_domain_name(self):
        domain_name = self.get_available_domain_name(suffix=".com")

        response = self.client.domain_delete(domain_name)

        return response

    @test_with_name("Domain delete with unexisting domain")
    @expect(2303, "Object does not exist")
    def test_domain_delete_non_existing_domain(self):
        domain_name = self.get_available_domain_name()

        response = self.client.domain_delete(domain_name)

        return response

    @test_with_name("Domain delete on domain with redemptionPeriod status")
    @expect(2304, "The operation is prohibited")
    def test_domain_delete_status_prohibits_operation(self):
        domain_name = self.get_available_domain_name()
        response = self.client.domain_create(domain_name, 1, [], self.perm_contacts[0], [])

        if get_code(response) != 1000:
            raise RuntimeError(f"Could not create \"{domain_name}\"")
        response = self.client.domain_delete(domain_name)

        if get_code(response) not in (1000, 1001):
            raise RuntimeError(f"Could not delete \"{domain_name}\"")

        response = self.client.domain_delete(domain_name)

        return response

    @test_with_name("Domain delete on domain that's associated to host")
    @expect(2305, "Object association prohibits operation")
    def test_domain_delete_association_prohibits_operation(self):
        domain_name = self.get_available_domain_name()
        response = self.client.domain_create(domain_name, 1, [], self.perm_contacts[0], [])
        self.domains_to_delete.append(domain_name)

        if get_code(response) != 1000:
            raise RuntimeError(f"Could not create domain \"{domain_name}\"")

        host_name = "ns1." + domain_name
        response = self.client.host_create(host_name, "1.1.1.1")
        self.hosts_to_delete.append(host_name)

        if get_code(response) not in (1000, 1001):
            raise RuntimeError(f"Could not create host \"{host_name}\"")

        response = self.client.domain_delete(domain_name)

        return response

    @test_with_name("Domain renew with too long period")
    @expect(2004, "Period exceeded the maximum value")
    def test_domain_renew_too_long_result_period(self):
        domain_name = self.get_available_domain_name()
        response = self.client.domain_create(domain_name, 1, [], self.perm_contacts[0], [])
        self.domains_to_delete.append(domain_name)

        if get_code(response) != 1000:
            raise RuntimeError(f"Could not create \"{domain_name}\"")

        response = self.client.domain_info(domain_name)
        cur_date = get_exp_date(response)

        response = self.client.domain_renew(domain_name, cur_date, 10)

        return response

    @test_with_name("Domain renew with syntax error")
    @expect(2001,
            "Element \'{http://hostmaster.ua/epp/domain-1.1}period\': \'-1\' is not a valid value of the atomic type \'{http://hostmaster.ua/epp/domain-1.1}pLimitType\'.")
    def test_domain_renew_syntax_error(self):
        domain_name = self.get_available_domain_name()

        response = self.client.domain_renew(domain_name, "2025-01-01", -1)

        return response

    @test_with_name("Domain renew with value syntax error")
    @expect(2005,
            "Incorrect domain name")
    def test_domain_renew_syntax_error(self):
        response = self.client.domain_renew("$%!@", "2001-10-10", 1)

        return response

    @test_with_name("Domain renew with wrong expire date")
    @expect(2105, "incorrect element domain:curExpDate")
    def test_domain_renew_wrong_expire_date(self):
        domain_name = self.get_available_domain_name()
        response = self.client.domain_create(domain_name, 1, [], self.perm_contacts[0], [])
        self.domains_to_delete.append(domain_name)

        if get_code(response) != 1000:
            raise RuntimeError(f"Could not create \"{domain_name}\"")

        response = self.client.domain_renew(domain_name, "1970-01-01", 1)

        return response

    @test_with_name("Domain renew with unexisting domain")
    @expect(2303, "Object does not exist")
    def test_domain_renew_unexisting_domain(self):
        domain_name = self.get_available_domain_name()

        response = self.client.domain_renew(domain_name, "1970-01-01", 1)

        return response

    @test_with_name("Domain renew on domain with redemptionPeriod status")
    @expect(2304, "Object status prohibits operation")
    def test_domain_renew_deleted_domain(self):
        domain_name = self.get_available_domain_name()
        response = self.client.domain_create(domain_name, 1, [], self.perm_contacts[0], [])

        if get_code(response) != 1000:
            raise RuntimeError(f"Could not create \"{domain_name}\"")

        response = self.client.domain_delete(domain_name)

        if get_code(response) not in (1000, 1001):
            raise RuntimeError(f"Could not delete \"{domain_name}\"")

        response = self.client.domain_renew(domain_name, "1970-01-01", 1)

        return response

    @test_with_name("Domain update with value syntax error")
    @expect(2001,
            "Element \'{http://hostmaster.ua/epp/domain-1.1}update\': Missing child element(s). Expected is ( {http://hostmaster.ua/epp/domain-1.1}name ).")
    def test_domain_update_syntax_error(self):
        response = self.client.send_xml(domain_update_without_domain_name({}, {}, {}))

        return response

    @test_with_name("Domain update with value syntax error")
    @expect(2005, "Incorrect domain name")
    def test_domain_update_value_syntax_error(self):
        response = self.client.domain_update("!@@%", {}, {}, {})

        return response

    @test_with_name("Domain update with unexisting domain")
    @expect(2303, "Object does not exist")
    def test_domain_update_unexisting_domain(self):
        domain_name = self.get_available_domain_name()

        response = self.client.domain_update(domain_name, {}, {}, {})

        return response

    @test_with_name("Domain update on domain with redemptionPeriod status")
    @expect(2304, "The operation is prohibited")
    def test_domain_update_deleted_domain(self):
        domain_name = self.get_available_domain_name()
        response = self.client.domain_create(domain_name, 1, [], self.perm_contacts[0], [])

        if get_code(response) != 1000:
            raise RuntimeError(f"Could not create \"{domain_name}\"")

        response = self.client.domain_delete(domain_name)

        if get_code(response) not in (1000, 1001):
            raise RuntimeError(f"Could not delete \"{domain_name}\"")

        response = self.client.domain_update(domain_name, {}, {}, {"registrant": "123"})

        return response

    @test_with_name("Domain restore with value syntax error")
    @expect(2001,
            "Element \'{http://hostmaster.ua/epp/domain-1.1}update\': Missing child element(s). Expected is ( {http://hostmaster.ua/epp/domain-1.1}name ).")
    def test_domain_restore_syntax_error(self):
        response = self.client.send_xml(domain_restore_without_domain_name())

        return response

    @test_with_name("Domain restore with value syntax error")
    @expect(2005, "Incorrect domain name")
    def test_domain_restore_value_syntax_error(self):
        response = self.client.domain_restore("!@@%")

        return response

    @test_with_name("Domain restore with unexisting domain")
    @expect(2303, "Object does not exist")
    def test_domain_restore_unexisting_domain(self):
        domain_name = self.get_available_domain_name()

        response = self.client.domain_restore(domain_name)

        return response

    @test_with_name("Domain restore on domain without redemptionPeriod status")
    @expect(2304, "The operation is prohibited")
    def test_domain_restore_not_deleted_domain(self):
        domain_name = self.get_available_domain_name()
        response = self.client.domain_create(domain_name, 1, [], self.perm_contacts[0], [])
        self.domains_to_delete.append(domain_name)

        if get_code(response) != 1000:
            raise RuntimeError(f"Could not create \"{domain_name}\"")

        response = self.client.domain_restore(domain_name)

        return response

    @test_with_name("Domain restore with now empty change block")
    @expect(2306, "incorrect element")
    def test_domain_restore_with_chg_block(self):
        domain_name = self.get_available_domain_name()
        response = self.client.domain_create(domain_name, 1, [], self.perm_contacts[0], [])
        self.domains_to_delete.append(domain_name)

        if get_code(response) != 1000:
            raise RuntimeError(f"Could not create \"{domain_name}\"")

        response = self.client.domain_delete(domain_name)

        if get_code(response) not in (1000, 1001):
            raise RuntimeError(f"Could not delete \"{domain_name}\"")

        response = self.client.send_xml(domain_restore_with_change_block(domain_name))

        return response
