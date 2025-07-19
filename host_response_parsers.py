import xml.etree.ElementTree as ET

# parsers that are used only for printing in console

def parse_host_check_response(xml_string):
    root = ET.fromstring(xml_string)

    ns = {
        'epp': 'urn:ietf:params:xml:ns:epp-1.0',
        'host': 'http://hostmaster.ua/epp/host-1.1'
    }

    for cd in root.findall('.//host:cd', ns):
        name_el = cd.find('host:name', ns)
        name = name_el.text
        avail = name_el.attrib.get('avail')
        print(f"{name} - {'available' if avail == '1' else 'unavailable'}")
        reason_el = cd.find('host:reason', ns)
        if reason_el is not None:
            print(f"  Reason: {reason_el.text}")

def parse_host_create_response(xml_string):
    root = ET.fromstring(xml_string)
    ns = {"epp": "urn:ietf:params:xml:ns:epp-1.0"}

    result = root.find(".//epp:result", ns)
    if result is not None:
        code = result.get("code")
        msg = result.find("epp:msg", ns)
        if msg is not None:
            print(f"Status code: {code}")
            print(f"Message: {msg.text}")
        else:
            print(f"Status code: {code}")
            print("No message found.")
    else:
        print("No <result> found in the response.")