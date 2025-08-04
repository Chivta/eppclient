import xml.etree.ElementTree as ET
from xml.etree.ElementTree import Element

from config import NAMESPACES

def parse_result_element(root: Element|str) -> str:
    if type(root) == str:
        root = ET.fromstring(root)
    result = root.find('.//epp:result', NAMESPACES)
    if result is not None:
        code = result.attrib.get('code')
        msg = result.find('epp:msg', NAMESPACES)
        print(f"[+] Response code: {code}")
        if msg is not None:
            print(f"[*] Message: {msg.text}")
        return code
    return "2000"


def get_code(xml_string: str) -> int:
    root = ET.fromstring(xml_string)
    result = root.find('.//epp:result', NAMESPACES)

    if result is not None:
        code = result.attrib.get('code')
        return int(code)
    raise Exception("Invalid argument")


def get_code_and_message(xml_string: str) -> tuple[int, str]:
    root = ET.fromstring(xml_string)
    result = root.find('.//epp:result', NAMESPACES)

    if result is not None:
        code = result.attrib.get('code')
        msg = result.find('epp:msg', NAMESPACES)
        return int(code), msg.text
    raise Exception("Invalid argument")


def save_req(req: str):
    with open("req.xml", "w") as f:
        f.write(req)


def save_response(resp, filename="resp.xml"):
    with open(filename, "w") as f:
        f.write(resp)


def get_error_reason(xml_string) -> str:
    try:
        root = ET.fromstring(xml_string)

        # Find the <result> element and get its code
        result = root.find('.//epp:result', namespaces=NAMESPACES)
        if result is None:
            return None

        code_str = result.attrib.get("code")
        if code_str is None or int(code_str) < 2000:
            return None  # Not an error

        # Find <extValue> inside <result>
        ext_value = result.find('epp:extValue', namespaces=NAMESPACES)
        if ext_value is None:
            return None

        # Find <reason> inside <extValue>
        reason = ext_value.find('epp:reason', namespaces=NAMESPACES)
        if reason is not None and reason.text:
            return reason.text.strip()

        return None

    except ET.ParseError:
        return None


def validate_code_and_reason(response, expected_code, expected_reason):
    reason = get_error_reason(response)

    code, message = get_code_and_message(response)
    if code == expected_code:
        if reason == expected_reason:
            return True, ""
        return False, "Expected reason: " + expected_reason + " instead got: " + reason

    return False, message


def get_exp_date(xml_string):
    try:
        root = ET.fromstring(xml_string)
        exp_date = root.find(".//domain:exDate", namespaces=NAMESPACES)
        if exp_date is None:
            return None
        return exp_date.text

    except ET.ParseError:
        return None

def domain_exists(domain_info: str) -> bool:
    root = ET.fromstring(domain_info)
    return
