import xml.etree.ElementTree as ET
from config import namespaces
from response_parsers.general_func import parse_result_element

# response_parsers that are used only for printing in console

def parse_host_check_response(xml_string):
    root = ET.fromstring(xml_string)

    # Parse result
    parse_result_element(root)

    cds = root.findall('.//host:cd', namespaces)
    if cds:
        print("[*] Host check results:")
        for cd in cds:
            name_el = cd.find('host:name', namespaces)
            name = name_el.text
            avail = name_el.attrib.get('avail')
            print(f"  [+] {name} - {'available' if avail == '1' else 'unavailable'}")
            reason_el = cd.find('host:reason', namespaces)
            if reason_el is not None:
                print(f"      [+] Reason: {reason_el.text}")

def parse_host_create_response(xml_string):
    root = ET.fromstring(xml_string)

    # Parse result
    parse_result_element(root)


def parse_host_info_response(xml_string):
    root = ET.fromstring(xml_string)

    # Parse result
    parse_result_element(root)

    # Parse host info
    inf_data = root.find('.//host:infData', namespaces)
    if inf_data is None:
        print("[!] No <host:infData> section found.")
        return

    print("[+] Host Information:")

    name = inf_data.findtext('host:name', default='', namespaces=namespaces)
    if name:
        print(f"  [+] Host name: {name}")

    roid = inf_data.findtext('host:roid', default='', namespaces=namespaces)
    if roid:
        print(f"  [+] ROID: {roid}")

    statuses = inf_data.findall('host:status', namespaces)
    if statuses:
        print("  [*] Statuses:")
        for status in statuses:
            s_val = status.attrib.get('s', '')
            print(f"    [+] {s_val}")

    addrs = inf_data.findall('host:addr', namespaces)
    if addrs:
        print("  [*] IP Addresses:")
        for addr in addrs:
            ip_type = addr.attrib.get('ip', '')
            ip_value = addr.text
            print(f"    [+] {ip_type.upper()}: {ip_value}")

    clid = inf_data.findtext('host:clID', default='', namespaces=namespaces)
    if clid:
        print(f"  [+] Client ID: {clid}")

    crid = inf_data.findtext('host:crID', default='', namespaces=namespaces)
    if crid:
        print(f"  [+] Creator ID: {crid}")

    crdate = inf_data.findtext('host:crDate', default='', namespaces=namespaces)
    if crdate:
        print(f"  [+] Creation Date: {crdate}")

    upid = inf_data.findtext('host:upID', default=None, namespaces=namespaces)
    if upid:
        print(f"  [+] Updater ID: {upid}")

    update = inf_data.findtext('host:upDate', default=None, namespaces=namespaces)
    if update:
        print(f"  [+] Last Updated: {update}")

    trdate = inf_data.findtext('host:trDate', default=None, namespaces=namespaces)
    if trdate:
        print(f"  [+] Transfer Date: {trdate}")
