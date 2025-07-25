import xml.etree.ElementTree as ET
from xml.etree.ElementTree import Element

from config import ns

def parse_result_element(root: Element) -> str:
    result = root.find('.//epp:result', ns)
    if result is not None:
        code = result.attrib.get('code')
        msg = result.find('epp:msg', ns)
        print(f"[+] Response code: {code}")
        if msg is not None:
            print(f"[*] Message: {msg.text}")
        return code
    return "2000"

def get_code_and_message(xml_string : str) -> tuple[int,str]:
    root = ET.fromstring(xml_string)
    result = root.find('.//epp:result',ns)

    if result is not None:
        code = result.attrib.get('code')
        msg = result.find('epp:msg', ns)
        return int(code),msg.text
    raise Exception("Invalid argument")