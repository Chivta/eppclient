HOST = "test-epp.hostmaster.ua"
PORT = 700

NAMESPACES = {
    'epp': 'urn:ietf:params:xml:ns:epp-1.0',
    'domain': 'http://hostmaster.ua/epp/domain-1.1',
    'host': "http://hostmaster.ua/epp/host-1.1",
    'contact':"http://hostmaster.ua/epp/contact-1.1",
    'rgp':"http://hostmaster.ua/epp/rgp-1.1"
}

PERMANENT_DOMAINS = ["test-dom1.epp.ua"]
PERMANENT_CONTACTS = ["contact-1","contact-2","contact-3","contact-4","contact-5","contact-6","contact-7","contact-8","contact-9"]
PERMANENT_HOSTS = ["ns1.test-dom1.epp.ua"]

LOGIN = ""
PASSWORD = ""

CERTFILE = "client.pem"
KEYFILE = "client.key"
