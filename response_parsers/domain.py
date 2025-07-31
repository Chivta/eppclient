import xml.etree.ElementTree as ET
from config import namespaces
from response_parsers.general_func import parse_result_element
# response_parsers that are used only for printing in console

def parse_domain_info(xml_string):
    root = ET.fromstring(xml_string)

    # Parse result
    parse_result_element(root)

    for inf_data in root.findall('.//domain:infData', namespaces):
        print("[*] Domain Information:")
        print("  Name:", inf_data.findtext('domain:name', default='N/A', namespaces=namespaces))
        print("  ROID:", inf_data.findtext('domain:roid', default='N/A', namespaces=namespaces))

        statuses = inf_data.findall('domain:status', namespaces)
        for status in statuses:
            print("  Status:", status.attrib.get('s'))

        print("  Registrant:", inf_data.findtext('domain:registrant', default='N/A', namespaces=namespaces))

        for contact in inf_data.findall('domain:contact', namespaces):
            print(f"  Contact ({contact.attrib.get('type')}):", contact.text)

        print("  Nameservers:")
        for host in inf_data.findall('domain:ns/domain:hostObj', namespaces):
            print("    -", host.text)

        for host in inf_data.findall('domain:host', namespaces):
            print("  Host:", host.text)

        print("  clID:", inf_data.findtext('domain:clID', default='N/A', namespaces=namespaces))
        print("  crID:", inf_data.findtext('domain:crID', default='N/A', namespaces=namespaces))
        print("  crDate:", inf_data.findtext('domain:crDate', default='N/A', namespaces=namespaces))
        print("  upID:", inf_data.findtext('domain:upID', default='N/A', namespaces=namespaces))
        print("  upDate:", inf_data.findtext('domain:upDate', default='N/A', namespaces=namespaces))
        print("  exDate:", inf_data.findtext('domain:exDate', default='N/A', namespaces=namespaces))
        print("  Auth Info PW:", inf_data.findtext('domain:authInfo/domain:pw', default='N/A', namespaces=namespaces))

def parse_domain_check_response(xml_string):
    root = ET.fromstring(xml_string)
    # Parse result
    parse_result_element(root)

    for cd in root.findall('.//domain:cd', namespaces):
        name_elem = cd.find('domain:name', namespaces)
        name = name_elem.text
        avail = name_elem.attrib['avail']
        reason_elem = cd.find('domain:reason', namespaces)
        reason = reason_elem.text if reason_elem is not None else "Available"
        status = "Available" if avail == "1" else "Not Available"
        print(f"[*] {name}: {status} ({reason})")

def parse_domain_create_response(xml_string):
    root = ET.fromstring(xml_string)
    # Parse result
    code = parse_result_element(root)

    if code == "1000":
        cre_data = root.find('.//domain:creData', namespaces)
        if cre_data is not None:
            name = cre_data.findtext('domain:name', default='N/A', namespaces=namespaces)
            cr_date = cre_data.findtext('domain:crDate', default='N/A', namespaces=namespaces)
            ex_date = cre_data.findtext('domain:exDate', default='N/A', namespaces=namespaces)
            print(f"[*] Domain Created: {name}")
            print(f"[*] Created At: {cr_date}")
            print(f"[*] Expires At: {ex_date}")
        else:
            print("[!] No <domain:creData> found in successful response.")
    else:
        ext_value = root.find('.//epp:extValue', namespaces)
        if ext_value is not None:
            value_elem = ext_value.find('.//domain:hostObj', namespaces)
            reason_elem = ext_value.find('epp:reason', namespaces)
            value = value_elem.text.strip() if value_elem is not None else "?"
            reason = reason_elem.text if reason_elem is not None else "Unknown reason"
            print(f"[!] Error Element: {value}")
            print(f"[!] Reason: {reason}")
        else:
            print("[!] No <extValue> provided with the error.")

def parse_domain_delete_response(xml_response):
    root = ET.fromstring(xml_response)
    # Parse result
    parse_result_element(root)
