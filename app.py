from EPPStream import EPPStream
from config import *
from response_parsers.domain import *
from response_parsers.host import *
from response_parsers.contact import *
from EPPServerConnection import EPPServerConnection
from EPPClient import EPPClient

# creating a socket and wrapping in into a tls context
try:
    connection = EPPServerConnection(HOST, PORT, CERTFILE, KEYFILE)
except FileNotFoundError:
    print("Add client.key and client.pem files with private key and certificate respectively")
    exit()
except SSLError:
    print("Key does not match the certificate")
    exit()

epp_stream = EPPStream(connection)

epp_client = EPPClient(epp_stream)

if LOGIN=="" or PASSWORD=="":
    print("Enter client id and password in config.py file")
    exit()

data = {
    "cl_id": LOGIN,
    "password": PASSWORD,
}

def login():
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
    login()
    while True:
        print("1. Domain\n2. Host\n3. Contact\n0. Exit")
        choice = input("Choose an option: ").strip()
        action = main_menu_actions.get(choice)
        if action:
            action()
        else:
            print("Invalid choice. Try again.")
        print()

# ===  DOMAIN MENU  ===

def domain_create():
    print("=== Creating a domain ===")
    name = input("Enter domain name: ")
    name_servers = get_nameservers()
    registrant = input("Enter registrant: ")
    contacts = get_contacts()

    print(f"Creating domain: {name}")

    response = epp_client.domain_create(name, 1, name_servers, registrant, contacts)

    parse_domain_create_response(response)


def get_nameservers():
    print("Adding name servers")
    res = []
    while len(res) <= 10:
        usr_inp = input("1. Add existing host 2. Add new host 3. Stop adding name servers ")
        if usr_inp == "1":
            res.append(input("Enter host name: "))
        elif usr_inp == "2":
            name = input("Enter host name: ")
            ipv4 = input("Enter ipv4 or empty line for none: ")
            ipv6 = input("Enter ipv6 or empty line for none: ")
            res.append((name,{"v4":ipv4,"v6":ipv6}))
        elif usr_inp == "" or usr_inp == "3":
            break

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


def domain_delete():
    print("=== Domain delete ===")
    domain = input("Enter domain name: ")

    response = epp_client.domain_delete(domain)

    parse_domain_delete_response(response)

def domain_renew():
    print("=== Domain renew ===")
    domain = input("Enter domain name: ")
    response = epp_client.domain_info(domain)

    exp_date = get_exp_date(response)
    if exp_date is None:
        print("Domain does not exist")
    exp_date = exp_date[:10]
    print(f"Domain has expire date \"{exp_date}\"")

    new_period = input("Enter how many years to extend the domain’s expiration date: ")

    if not new_period.isdigit():
        print("Invalid period input")
        return

    response = epp_client.domain_renew(domain, exp_date, int(new_period))

    parse_domain_renew_response(response)


domain_menu_actions = {
    "1": domain_check,
    "2": domain_info,
    "3": domain_create,
    "4": domain_delete,
    "5": domain_renew,
    # "6": domain_transfer,
    # "7": domain_update,
    # "8": domain_restore,
}

def domain_menu():
    while True:
        print("1. Domain check\n"
              "2. Domain info\n"
              "3. Domain create\n"
              "4. Domain delete\n"
              "5. Domain renew\n"
              "6. Domain transfer\n"
              "7. Domain update\n"
              "8. Domain restore"
              )
        choice = input("Choose an option: ").strip()
        action = domain_menu_actions.get(choice)
        if action:
            action()
        elif choice == len(domain_menu_actions)+1:
            return
        else:
            print("Invalid choice.")
        print()

# ===  HOST MENU  ===
def host_menu():
    while True:
        print("1. Host check\n2. Host info\n3. Host create\n4. Exit")
        choice = input("Choose an option: ").strip()
        action = host_menu_actions.get(choice)
        if action:
            action()
        elif choice == "4":
            return
        else:
            print("Invalid choice.\n")
        print()

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

def host_info():
    print("=== Host Info ===")
    name = input("Enter host name: ")

    response = epp_client.host_info(name)

    parse_host_info_response(response)


host_menu_actions = {
    "1":host_check,
    "2":host_info,
    "3":host_create,
}

# ===  CONTACT MENU  ===

def contact_menu():
    while True:
        print("1. Contact check\n2. Contact info\n3. Contact create\n4. Contact delete\n5. Exit")
        choice = input("Choose an option: ").strip()
        action = contact_menu_actions.get(choice)
        if action:
            action()
        elif choice == "5":
            return
        else:
            print("Invalid choice.\n")
        print()

def contact_check():
    print("=== Contact check ===")
    contacts = []
    while len(contacts) <= 10:
        contact = input("Enter host name or q to stop: ")
        if (contact == "" or contact == "q"):
            break

        contacts.append(contact)
    response = epp_client.contact_check(contacts)
    parse_contact_check_response(response)

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
    _password = input("Enter PASSWORD: ")

    print(f"Creating contact: {contact_id}")
    response = epp_client.contact_create(contact_id, name, city, country_code, email, _password)
    parse_host_create_response(response)

def contact_delete():
    print("=== Contact delete ===")
    contact_id = input("Enter contact id: ")

    response = epp_client.contact_delete(contact_id)

    parse_contact_delete(response)

contact_menu_actions = {
    "1": contact_check,
    "2": contact_info,
    "3": contact_create,
    "4": contact_delete
}


main_menu_actions = {
    "1": domain_menu,
    "2": host_menu,
    "3": contact_menu,
    "0": unlog_and_exit
}

if __name__ == "__main__":
    main()