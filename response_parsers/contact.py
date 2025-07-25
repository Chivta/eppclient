import xml.etree.ElementTree as ET
from config import ns
from response_parsers.general_func import parse_result_element

# response_parsers that are used only for printing in console

def parse_host_create_response(xml_string):
    root = ET.fromstring(xml_string)
    # Parse result
    parse_result_element(root)

def parse_contact_info(xml_string):
    root = ET.fromstring(xml_string)

    # Parse result
    code = parse_result_element(root)

    # Skip parsing if result code starts with '2' (error)
    if code.startswith("2"):
        return

    inf_data = root.find('.//contact:infData', ns)
    if inf_data is None:
        print("[!] No <contact:infData> section found.")
        return

    def get_text(tag):
        el = inf_data.find(f'contact:{tag}', ns)
        return el.text if el is not None else "N/A"

    print("[*] Contact Info:")
    print(f"    - ID: {get_text('id')}")
    print(f"    - ROID: {get_text('roid')}")

    status = inf_data.find('contact:status', ns)
    if status is not None:
        print(f"    - Status: {status.attrib.get('s')}")

    # Postal Info (both int and loc)
    for pi in inf_data.findall('contact:postalInfo', ns):
        ptype = pi.attrib.get('type')
        print(f"[*] Postal Info ({ptype}):")
        name = pi.findtext('contact:name', default='', namespaces=ns)
        org = pi.findtext('contact:org', default='', namespaces=ns)
        print(f"    - Name: {name}")
        print(f"    - Org: {org}")
        addr = pi.find('contact:addr', ns)
        if addr is not None:
            street = [s.text for s in addr.findall('contact:street', ns)]
            city = addr.findtext('contact:city', default='', namespaces=ns)
            pc = addr.findtext('contact:pc', default='', namespaces=ns)
            cc = addr.findtext('contact:cc', default='', namespaces=ns)
            print(f"    - Street: {' / '.join(street)}")
            print(f"    - City: {city}")
            print(f"    - Postal Code: {pc}")
            print(f"    - Country Code: {cc}")

    print(f"[*] Phone: {get_text('voice')}")
    print(f"[*] Email: {get_text('email')}")
    print(f"[*] Client ID: {get_text('clID')}")
    print(f"[*] Creator ID: {get_text('crID')}")
    print(f"[*] Creation Date: {get_text('crDate')}")

    # AuthInfo
    auth_pw = inf_data.findtext('contact:authInfo/contact:pw', default='N/A', namespaces=ns)
    print(f"[*] Auth Info PW: {auth_pw}")

    # Disclose Info
    disclose = inf_data.find('contact:disclose', ns)
    if disclose is not None:
        print("[*] Disclose Info:")
        flag = disclose.attrib.get('flag')
        print(f"    - Flag: {flag}")
        for child in disclose:
            tag = child.tag.split('}')[1]
            dtype = child.attrib.get('type')
            if dtype:
                print(f"    - {tag} (type={dtype})")
            else:
                print(f"    - {tag}")

def parse_contact_delete(xml_string):
    root = ET.fromstring(xml_string)

    # Parse result
    parse_result_element(root)