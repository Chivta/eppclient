from config import *
from domain_response_parsers import *
from host_response_parsers import *
from contact_response_parser import *
from EPPServerConnection import EPPServerConnection
from EPPClient import EPPClient

# creating a socket and wrapping in into a tls context
connection = EPPServerConnection(HOST, PORT, "client.pem", "client.key")
connection.handshake()
epp_client = EPPClient(connection)


data = {
    "cl_id": user_login,
    "password": password,
}

response = epp_client.login(**data)

if '<result code="1000">' not in response:
    print("Could not login")
    exit()

def unlog_and_exit():
    epp_client.logout()
    connection.close()
    exit()


# console app main entry
def main():
    while True:
        print("1. Domain\n2. Host\n3. Contact\n0. Exit")
        choice = input("Choose an option: ").strip()
        action = main_menu_actions.get(choice)
        if action:
            action()
        else:
            print("Invalid choice. Try again.\n")


# ===  DOMAIN MENU  ===

def domain_menu():
    while True:
        print("1. Domain check\n2. Domain info\n3. Domain create\n4. Back")
        choice = input("Choose an option: ").strip()
        action = domain_menu_actions.get(choice)
        if action:
            action()
        elif choice == "4":
            return
        else:
            print("Invalid choice.\n")


def domain_create():
    print("=== Creating a domain ===")
    name = input("Enter domain name: ")
    ns = get_nameservers()
    registrant = input("Enter registrant: ")
    contacts = get_contacts()
    # ... gather other fields
    print(f"Creating domain: {name}")

    response = epp_client.domain_create(name, 1, ns, registrant, contacts)

    parse_domain_create_response(response)


def get_nameservers():
    res = []
    while len(res) <= 10:
        usr_inp = input("Enter name server or q to quit:")
        if (usr_inp == "" or usr_inp == "q"):
            break

        res.append(usr_inp)

    return res


def get_contacts():
    res = []
    while True:
        usr_inp1 = input("Enter contact type or q to stop:")
        if (usr_inp1 == "" or usr_inp1 == "q"):
            break
        usr_inp2 = input("Enter contact or q to stop:")
        if (usr_inp2 == "" or usr_inp2 == "q"):
            break

        res.append((usr_inp1, usr_inp2))

    return res


def domain_check():
    print("=== Domain check ===")
    domains = []
    while len(domains) <= 10:
        name = input("Enter domain name or q to stop: ")
        if (name == "" or name == "q"):
            break

        domains.append(name)
    response = epp_client.domain_check(domains)

    parse_domain_check_response(response)


def domain_info():
    print("=== Domain info ===")
    domain = input("Enter domain name: ")

    response = epp_client.domain_info(domain)

    parse_domain_info(response)


domain_menu_actions = {
    "1": domain_check,
    "2": domain_info,
    "3": domain_create,
}

# ===  HOST MENU  ===
def host_menu():
    while True:
        print("1. Host check\n2. Host create\n3. Back")
        choice = input("Choose an option: ").strip()
        action = host_menu_actions.get(choice)
        if action:
            action()
        elif choice == "3":
            return
        else:
            print("Invalid choice.\n")

def host_check():
    print("=== Host check ===")
    hosts = []
    while len(hosts) <= 10:
        host = input("Enter host name or q to stop: ")
        if (host == "" or host == "q"):
            break

        hosts.append(host)
    response = epp_client.host_check(hosts)

    parse_host_check_response(response)

def host_create():
    print("=== Creating a Host ===")
    name = input("Enter host name: ")
    ipv4 = input("Enter ipv4 or empty line for none: ")
    ipv6 = input("Enter ipv6 or empty line for none: ")

    print(f"Creating host: {name}")

    response = epp_client.host_create(name, ipv4,ipv6)

    parse_host_create_response(response)

host_menu_actions = {
    "1":host_check,
    "2":host_create
}

# ===  CONTACT MENU  ===

def contact_menu():
    while True:
        print("1. Contact info\n2. Contact create\n3. Back")
        choice = input("Choose an option: ").strip()
        action = contact_menu_actions.get(choice)
        if action:
            action()
        elif choice == "3":
            return
        else:
            print("Invalid choice.\n")

def contact_info():
    print("=== Contact check ===")
    contact_id = input("Enter contact id: ")

    response = epp_client.contact_info(contact_id)

    parse_contact_info(response)

def contact_create():
    print("=== Creating a contact ===")
    contact_id = input("Enter contact id: ")
    name = input("Enter contact name: ")
    city = input("Enter city: ")
    country_code = input("Enter country code: ")
    email = input("Enter email: ")
    _password = input("Enter password: ")

    print(f"Creating contact: {contact_id}")
    response = epp_client.contact_create(contact_id, name, city, country_code, email, _password)
    parse_host_create_response(response)

contact_menu_actions = {
    "1": contact_info,
    "2": contact_create
}


main_menu_actions = {
    "1": domain_menu,
    "2": host_menu,
    "3": contact_menu,
    "0": unlog_and_exit
}

if __name__ == "__main__":
    main()