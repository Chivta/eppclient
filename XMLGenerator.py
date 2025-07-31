# XML templates for requests
from config import ns

def wrap_in_epp_element(content: str) -> str:
    return f'''<?xml version="1.0" encoding="UTF-8" standalone="no"?>
 <epp xmlns="{ns["epp"]}">
    {content}
 </epp>'''


def login(cl_id: str, password: str) -> str:
    return wrap_in_epp_element(f'''
  <command>
    <login>
      <clID>{cl_id}</clID>
      <pw>{password}</pw>
      <options>
        <version>1.0</version>
        <lang>en</lang>
      </options>
      <svcs>
        <objURI>urn:ietf:params:xml:ns:epp-1.0</objURI>
        <objURI>http://hostmaster.ua/epp/contact-1.1</objURI>
        <objURI>http://hostmaster.ua/epp/domain-1.1</objURI>
        <objURI>http://hostmaster.ua/epp/host-1.1</objURI>
        <svcExtension>
          <extURI>http://hostmaster.ua/epp/rgp-1.1</extURI>
          <extURI>http://hostmaster.ua/epp/uaepp-1.1</extURI>
          <extURI>http://hostmaster.ua/epp/balance-1.0</extURI>
          <extURI>http://hostmaster.ua/epp/secDNS-1.1</extURI>
        </svcExtension>
      </svcs>
    </login>
  </command>''')


def logout() -> str:
    return wrap_in_epp_element(f'''
  <command>
    <logout/>
  </command>''')

def domain_check(domains: list[str]) -> str:
    return wrap_in_epp_element(f'''
    <command>
     <check>
       <domain:check xmlns:domain="http://hostmaster.ua/epp/domain-1.1">
         {"".join(f"<domain:name>{domain}</domain:name>" for domain in domains)}
       </domain:check>
     </check>
   </command>''')

def hello() -> str:
    return wrap_in_epp_element('''
   <hello/>''')

def build_hosts(ns : list) -> str:
    if not ns: return ""
    result = "<domain:ns>\n"

    for serv in ns:
        if type(serv) == str:
            result += f'{f"<domain:hostObj>{serv}</domain:hostObj>"}'
        elif type(serv) == tuple:
            result += "<domain:hostAttr>\n"
            result += f"<domain:hostName>{serv[0]}</domain:hostName>\n"
            for v, adr in serv[1].items():
                if adr:
                    result += f'<domain:hostAddr ip="{v}">{adr}</domain:hostAddr>\n'
            result += "</domain:hostAttr>\n"

    result += "</domain:ns>"
    return result

def domain_info(domain: str) -> str:
    return wrap_in_epp_element(f'''
    <command>
        <info>
          <domain:info xmlns:domain="http://hostmaster.ua/epp/domain-1.1">
            <domain:name>{domain}</domain:name>
          </domain:info>
        </info>
    </command>''')

def domain_create(name : str, period : int, ns, registrant : str, contacts : list[tuple[str, str]]) -> str:
    return wrap_in_epp_element(f'''
    <command>
      <create>
        <domain:create xmlns:domain="http://hostmaster.ua/epp/domain-1.1">
          <domain:name>{name}</domain:name>
          <domain:period unit="y">{period}</domain:period>
            {build_hosts(ns)}
          <domain:registrant>{registrant}</domain:registrant>
          {"\n".join(f'<domain:contact type="{type_}">{text}</domain:contact>' for type_, text in contacts)}
        </domain:create>
      </create>
    </command>''')

def host_check(hosts) -> str:
    return wrap_in_epp_element(f'''
   <command>
     <check>
       <host:check xmlns:host="http://hostmaster.ua/epp/host-1.1">
         {"\n".join(f"<host:name>{host}</host:name>" for host in hosts) }
       </host:check>
     </check>
   </command>''')

def contact_info(contact) -> str:
    return wrap_in_epp_element(f'''
   <command>
     <info>
       <contact:info xmlns:contact="http://hostmaster.ua/epp/contact-1.1">
         <contact:id>{contact}</contact:id>
       </contact:info>
     </info>
   </command>''')


def host_create(name,ipv4,ipv6) -> str:
    return wrap_in_epp_element(f'''
    <command>
     <create>
       <host:create xmlns:host="http://hostmaster.ua/epp/host-1.1">
         <host:name>{name}</host:name>
           {f"<host:addr ip='v4'>{ipv4}</host:addr>" if ipv4 else ""}
           {f"<host:addr ip='v6'>{ipv6}</host:addr>" if ipv6 else ""}
       </host:create>
     </create>
   </command>''')


def contact_create(contact_id, name, city, country_code, email, password) -> str:
    return wrap_in_epp_element(f'''
    <command>
        <create>
          <contact:create xmlns:contact="http://hostmaster.ua/epp/contact-1.1">
            <contact:id>{contact_id}</contact:id>
            <contact:postalInfo type="int">
              <contact:name>{name}</contact:name>
              <contact:addr>
                <contact:city>{city}</contact:city>
                <contact:cc>{country_code}</contact:cc>
              </contact:addr>
            </contact:postalInfo>
            <contact:email>{email}</contact:email>
            <contact:authInfo>
              <contact:pw>{password}</contact:pw>
            </contact:authInfo>
          </contact:create>
        </create>
    </command>''')

def domain_delete(domain:str) -> str:
    return wrap_in_epp_element(f'''
    <command>
      <delete>
        <domain:delete xmlns:domain="http://hostmaster.ua/epp/domain-1.1">
          <domain:name>{domain}</domain:name>
        </domain:delete>
      </delete>
    </command>''')


def contact_delete(contact_id:str) -> str:
    return wrap_in_epp_element(f'''
    <command>
      <delete>
        <contact:delete xmlns:contact="http://hostmaster.ua/epp/contact-1.1">
          <contact:id>{contact_id}</contact:id>
        </contact:delete>
      </delete>
    </command>''')

def contact_check(contact_id:str) -> str:
    return wrap_in_epp_element(f'''
    <command>
     <check>
       <contact:check
        xmlns:contact="http://hostmaster.ua/epp/contact-1.1">
         <contact:id>{contact_id}</contact:id>
       </contact:check>
     </check>
   </command>''')

def host_info(name) -> str:
    return wrap_in_epp_element(f'''
    <command>
     <info>
       <host:info xmlns:host="http://hostmaster.ua/epp/host-1.1">
         <host:name>{name}</host:name>
       </host:info>
     </info>
   </command>''')