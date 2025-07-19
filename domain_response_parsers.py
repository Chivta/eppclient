import xml.etree.ElementTree as ET

# parsers that are used only for printing in console

def parse_domain_info(xml_string):
    ns = {
        'epp': 'urn:ietf:params:xml:ns:epp-1.0',
        'domain': 'http://hostmaster.ua/epp/domain-1.1'
    }

    root = ET.fromstring(xml_string)

    result = root.find('.//epp:result', ns)
    if result is not None:
        code = result.attrib.get('code')
        message = result.findtext('epp:msg', default='No message', namespaces=ns)
        if code != '1000':
            print("Error code:", code)
            print("Message:", message)
            return

    for inf_data in root.findall('.//domain:infData', ns):
        print("Domain Information:")
        print("  Name:", inf_data.findtext('domain:name', default='N/A', namespaces=ns))
        print("  ROID:", inf_data.findtext('domain:roid', default='N/A', namespaces=ns))

        statuses = inf_data.findall('domain:status', ns)
        for status in statuses:
            print("  Status:", status.attrib.get('s'))

        print("  Registrant:", inf_data.findtext('domain:registrant', default='N/A', namespaces=ns))

        for contact in inf_data.findall('domain:contact', ns):
            print(f"  Contact ({contact.attrib.get('type')}):", contact.text)

        print("  Nameservers:")
        for host in inf_data.findall('domain:ns/domain:hostObj', ns):
            print("    -", host.text)

        for host in inf_data.findall('domain:host', ns):
            print("  Host:", host.text)

        print("  clID:", inf_data.findtext('domain:clID', default='N/A', namespaces=ns))
        print("  crID:", inf_data.findtext('domain:crID', default='N/A', namespaces=ns))
        print("  crDate:", inf_data.findtext('domain:crDate', default='N/A', namespaces=ns))
        print("  upID:", inf_data.findtext('domain:upID', default='N/A', namespaces=ns))
        print("  upDate:", inf_data.findtext('domain:upDate', default='N/A', namespaces=ns))
        print("  exDate:", inf_data.findtext('domain:exDate', default='N/A', namespaces=ns))
        print("  Auth Info PW:", inf_data.findtext('domain:authInfo/domain:pw', default='N/A', namespaces=ns))

def parse_domain_check_response(xml_string):
    ns = {
        'epp': 'urn:ietf:params:xml:ns:epp-1.0',
        'domain': 'http://hostmaster.ua/epp/domain-1.1'
    }

    root = ET.fromstring(xml_string)
    result_code = root.find('.//epp:result', ns).attrib['code']
    message = root.find('.//epp:msg', ns).text
    print(f"Result Code: {result_code}")
    print(f"Message: {message}\n")

    for cd in root.findall('.//domain:cd', ns):
        name_elem = cd.find('domain:name', ns)
        name = name_elem.text
        avail = name_elem.attrib['avail']
        reason_elem = cd.find('domain:reason', ns)
        reason = reason_elem.text if reason_elem is not None else "Available"

        status = "Available" if avail == "1" else "Not Available"
        print(f"{name}: {status} ({reason})")

def parse_domain_create_response(xml_string):
    ns = {
        'epp': 'urn:ietf:params:xml:ns:epp-1.0',
        'domain': 'http://hostmaster.ua/epp/domain-1.1'
    }

    root = ET.fromstring(xml_string)
    result_elem = root.find('.//epp:result', ns)
    result_code = result_elem.attrib.get('code')
    message = result_elem.find('epp:msg', ns).text
    print(f"Result Code: {result_code}")
    print(f"Message: {message}\n")

    if result_code == "1000":
        # Success case
        cre_data = root.find('.//domain:creData', ns)
        if cre_data is not None:
            name = cre_data.find('domain:name', ns).text
            cr_date = cre_data.find('domain:crDate', ns).text
            ex_date = cre_data.find('domain:exDate', ns).text
            print(f"Domain Created: {name}")
            print(f"Created At: {cr_date}")
            print(f"Expires At: {ex_date}")
        else:
            print("No <domain:creData> found in successful response.")
    else:
        # Error case
        ext_value = root.find('.//epp:extValue', ns)
        if ext_value is not None:
            value_elem = ext_value.find('.//domain:hostObj', ns)
            reason_elem = ext_value.find('epp:reason', ns)
            value = value_elem.text.strip() if value_elem is not None else "?"
            reason = reason_elem.text if reason_elem is not None else "Unknown reason"
            print(f"Error Element: {value}")
            print(f"Reason: {reason}")
        else:
            print("No <extValue> provided with the error.")