from MalformXMLGenerator import domain_create_no_registrant, domain_update_without_domain_name, \
    domain_restore_without_domain_name, domain_restore_with_change_block, host_info_without_host_name, \
    host_create_without_host_name, host_delete_without_host_name
from general_func import get_code_and_message, get_error_reason, get_code, save_response, get_exp_date
from tests.base_tester import Tester, test_with_name, expect, generate_random_name


class HostTester(Tester):
    @test_with_name("Host check with too many hosts")
    @expect(2001, "Element \'{http://hostmaster.ua/epp/host-1.1}name\': This element is not expected.")
    def test_host_check_too_many_hosts(self) -> tuple[bool, str]:
        response = self.client.host_check([generate_random_name(6,".epp.ua") for _ in range(11)])

        return response

    @test_with_name("Host info with syntax error")
    @expect(2001, "Element \'{http://hostmaster.ua/epp/host-1.1}info\': Missing child element(s). Expected is ( {http://hostmaster.ua/epp/host-1.1}name ).")
    def test_host_info_syntax_error(self) -> tuple[bool, str]:
        response = self.client.send_xml(host_info_without_host_name())

        return response


    @test_with_name("Host info with value syntax error")
    @expect(2005, "Incorrect hostname")
    def test_host_info_value_syntax_error(self) -> tuple[bool, str]:
        response = self.client.host_info("!!!")

        return response

    @test_with_name("Host info of unexisting host")
    @expect(2303, "Object does not exist")
    def test_host_info_unexisting_host(self) -> tuple[bool, str]:
        host_name = self.get_available_host_name()
        response = self.client.host_info(host_name)

        return response

    @test_with_name("Host create with syntax error")
    @expect(2001, "Element \'{http://hostmaster.ua/epp/host-1.1}addr\': This element is not expected. Expected is ( {http://hostmaster.ua/epp/host-1.1}name ).")
    def test_host_create_syntax_error(self) -> tuple[bool, str]:
        response = self.client.send_xml(host_create_without_host_name("1.1.1.1",""))

        return response

    @test_with_name("Host create with value syntax error")
    @expect(2005,
            "Incorrect hostname")
    def test_host_create_value_syntax_error(self) -> tuple[bool, str]:
        response = self.client.host_create("!!!","1.1.1.1")

        return response

    @test_with_name("Host create without ips")
    @expect(2003,
            "IP not found")
    def test_host_create_no_ip(self) -> tuple[bool, str]:
        domain_name = self.get_available_domain_name()

        response = self.client.domain_create(domain_name,1,[],self.perm_contacts[0],[])
        self.domains_to_delete.append(domain_name)

        if get_code(response) != 1000:
            raise RuntimeError(f"Could not create {domain_name} domain")

        response = self.client.host_create(domain_name)
        self.hosts_to_delete.append(domain_name)
        return response

    @test_with_name("Host create with incorrect ip")
    @expect(2004,
            "Incorrect IP")
    def test_host_create_incorrect_ip(self) -> tuple[bool, str]:
        domain_name = self.get_available_domain_name()

        response = self.client.domain_create(domain_name, 1, [], self.perm_contacts[0], [])
        self.domains_to_delete.append(domain_name)

        if get_code(response) != 1000:
            raise RuntimeError(f"Could not create {domain_name} domain")

        response = self.client.host_create(domain_name,"1.0.0.256")
        self.hosts_to_delete.append(domain_name)
        return response

    @test_with_name("Host create with existing host")
    @expect(2302,
            "Object exists")
    def test_host_create_existing_host(self) -> tuple[bool, str]:
        domain_name = self.get_available_domain_name()

        response = self.client.domain_create(domain_name, 1, [], self.perm_contacts[0], [])
        self.domains_to_delete.append(domain_name)

        if get_code(response) != 1000:
            raise RuntimeError(f"Could not create {domain_name} domain")

        response = self.client.host_create(domain_name, "1.1.1.1")

        if get_code(response) != 1000:
            raise RuntimeError(f"Could not create {domain_name} host")

        response = self.client.host_create(domain_name, "1.1.1.1")

        self.hosts_to_delete.append(domain_name)
        return response

    @test_with_name("Host create without parent domain")
    @expect(2303,
            "Parent domain not exists")
    def test_host_create_no_parent_domain(self) -> tuple[bool, str]:
        host_name = self.get_available_host_name()

        response = self.client.host_create(host_name, "1.1.1.1")

        self.hosts_to_delete.append(host_name)
        return response

    @test_with_name("Host create bad external host")
    @expect(2306,
            "There are no data about server found")
    def test_host_create_bad_external_host(self) -> tuple[bool, str]:
        host_name = self.get_available_host_name(".com")

        response = self.client.host_create(host_name, "1.1.1.1")

        self.hosts_to_delete.append(host_name)
        return response

    @test_with_name("Host delete with syntax error")
    @expect(2001,
            "Element \'{http://hostmaster.ua/epp/host-1.1}delete\': Missing child element(s). Expected is ( {http://hostmaster.ua/epp/host-1.1}name ).")
    def test_host_delete_syntax_error(self) -> tuple[bool, str]:
        response = self.client.send_xml(host_delete_without_host_name())

        return response

    @test_with_name("Host delete with value syntax error")
    @expect(2005,
            "Incorrect hostname")
    def test_host_delete_value_syntax_error(self) -> tuple[bool, str]:
        response = self.client.host_delete("!!!")

        return response

    @test_with_name("Host delete on unexisting host")
    @expect(2305,
            "Object association prohibits operation")
    def test_host_delete_linked_host(self) -> tuple[bool, str]:
        domain_name = self.get_available_domain_name()
        response = self.client.domain_create(domain_name, 1, [self.perm_hosts[0]],self.perm_contacts[0],[])
        save_response(response)
        if get_code(response) != 1000:
            raise RuntimeError(f"Could not create {domain_name} domain")

        response = self.client.host_delete(self.perm_hosts[0])

        return response