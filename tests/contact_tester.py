from general_func import get_code
from tests.base_tester import Tester, test_with_name, expect, generate_random_name


class ContactTester(Tester):
    @test_with_name("Contact check with too many hosts")
    @expect(2001, "Element \'{http://hostmaster.ua/epp/contact-1.1}id\': This element is not expected.")
    def check_too_many_contacts(self) -> tuple[bool, str]:
        response = self.client.contact_check([generate_random_name(6) for _ in range(11)])

        return response

    @test_with_name("Contact info with syntax error")
    @expect(2001, "Element \'{http://hostmaster.ua/epp/contact-1.1}id\': [facet \'minLength\'] The value has a length of \'0\'; this underruns the allowed minimum length of \'3\'.")
    def info_syntax_error(self) -> tuple[bool, str]:
        response = self.client.contact_info("")

        return response

    @test_with_name("Contact info with value syntax error")
    @expect(2005,
            "Incorrect Contact ID")
    def info_value_syntax_error(self) -> tuple[bool, str]:
        response = self.client.contact_info("!!!")

        return response

    @test_with_name("Contact info with unexisting contact")
    @expect(2303,
            "Object does not exist")
    def info_unexisting_contact(self) -> tuple[bool, str]:
        contact_id = self.get_available_contact_name()

        response = self.client.contact_info(contact_id)

        return response

    @test_with_name("Contact create with syntax error")
    @expect(2001,
            "Element '{http://hostmaster.ua/epp/contact-1.1}postalInfo': This element is not expected. Expected is ( {http://hostmaster.ua/epp/contact-1.1}id ).")
    def create_syntax_error(self) -> tuple[bool, str]:
        response = self.client.contact_create("")

        return response

    @test_with_name("Contact create with syntax error")
    @expect(2005,
            "Incorrect Contact ID")
    def create_value_syntax_error(self) -> tuple[bool, str]:
        response = self.client.contact_create("!!!")

        return response

    # @test_with_name("Host info with required parameter missing")
    # @expect(2003,
    #         "Required parameter missing")
    # def create_required_parameter_missing(self) -> tuple[bool, str]:
    #     contact_id = self.get_available_contact_name()
    #
    #     response = self.client.contact_create("")
    #     self.contacts_to_delete.append(contact_id)
    #     # response = self.client.contact_create("")
    #
    #     return response

    @test_with_name("Contact create with existing object")
    @expect(2302,
            "Object exists")
    def create_object_exists(self) -> tuple[bool, str]:
        response = self.client.contact_create(self.perm_contacts[0])

        return response

    @test_with_name("Contact delete with syntax error")
    @expect(2001,
            "Element \'{http://hostmaster.ua/epp/contact-1.1}id\': [facet \'minLength\'] The value has a length of \'0\'; this underruns the allowed minimum length of \'3\'.")
    def delete_syntax_error(self) -> tuple[bool, str]:
        response = self.client.contact_delete("")

        return response

    @test_with_name("Contact delete with value syntax error")
    @expect(2005,
            "Incorrect Contact ID")
    def delete_value_syntax_error(self) -> tuple[bool, str]:
        response = self.client.contact_delete("!!!")

        return response

    @test_with_name("Contact delete with unexisting contact")
    @expect(2303,
            "Object does not exist")
    def delete_object_not_exists(self) -> tuple[bool, str]:
        contact_id = self.get_available_contact_name()

        response = self.client.contact_delete(contact_id)

        return response

    @test_with_name("Contact delete on contact with status clientDeleteProhibited")
    @expect(2304,
            "The operation is prohibited")
    def delete_status_prohibits_operation(self) -> tuple[bool, str]:
        self.client.contact_update(self.perm_contacts[0],{"statuses":["clientDeleteProhibited"]},{},{})

        response = self.client.contact_delete(self.perm_contacts[0])
        self.client.contact_update(self.perm_contacts[0],{},{"statuses":["clientDeleteProhibited"]},{})

        return response

    @test_with_name("Contact delete on contact linked to a domain")
    @expect(2305,
            "Object association prohibits operation")
    def delete_object_association_prohibits(self) -> tuple[bool, str]:
        domain_name = self.get_available_domain_name()
        self.domains_to_delete.append(domain_name)
        response = self.client.domain_create(domain_name,1,[],self.perm_contacts[0],[])
        if get_code(response) != 1000:
            raise RuntimeError("Could not create domain")

        response = self.client.contact_delete(self.perm_contacts[0])

        return response

    @test_with_name("Contact update with syntax error")
    @expect(2001,
            "Element \'{http://hostmaster.ua/epp/contact-1.1}id\': [facet \'minLength\'] The value has a length of \'0\'; this underruns the allowed minimum length of \'3\'.")
    def update_syntax_error(self) -> tuple[bool, str]:
        response = self.client.contact_update("",{},{},{})

        return response

    @test_with_name("Contact update with value syntax error")
    @expect(2005,
            "Incorrect Contact ID")
    def update_value_syntax_error(self) -> tuple[bool, str]:
        response = self.client.contact_update("!!!", {}, {}, {})

        return response

    @test_with_name("Contact update with unexisting contact")
    @expect(2303,
            "Object does not exist")
    def update_unexisting_contact(self) -> tuple[bool, str]:
        contact_id = self.get_available_contact_name()

        response = self.client.contact_update(contact_id, {}, {}, {})

        return response

    @test_with_name("Contact update on contact with status updateProhibited")
    @expect(2304,
            "The operation is prohibited")
    def update_status_prohibits_operation(self) -> tuple[bool, str]:
        self.client.contact_update(self.perm_contacts[0],{"statuses":["clientUpdateProhibited"]},{},{})

        response = self.client.contact_update(self.perm_contacts[0], {}, {}, {"name":"123"})

        self.client.contact_update(self.perm_contacts[0],{},{"statuses":["clientUpdateProhibited"]},{})

        return response