
# XML templates for requests

def login(cl_id: str, password: str) -> bytes:
    return f'''<?xml version="1.0" encoding="UTF-8" standalone="no"?>
<epp xmlns="urn:ietf:params:xml:ns:epp-1.0">
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
  </command>
</epp>'''.encode("utf-8")


def logout() -> bytes:
    return f'''<?xml version="1.0" encoding="UTF-8" standalone="no"?>
<epp xmlns="urn:ietf:params:xml:ns:epp-1.0">
  <command>
    <logout/>
  </command>
</epp>'''.encode("utf-8")

def domain_check(domains: list[str])-> bytes:
    return f'''<?xml version="1.0" encoding="UTF-8" standalone="no"?>
 <epp xmlns="urn:ietf:params:xml:ns:epp-1.0">
   <command>
     <check>
       <domain:check xmlns:domain="http://hostmaster.ua/epp/domain-1.1">
         {"".join(f"<domain:name>{domain}</domain:name>" for domain in domains)}
       </domain:check>
     </check>
   </command>
 </epp>'''.encode("utf-8")

def hello()-> bytes:
    return f'''
 <?xml version="1.0" encoding="UTF-8" standalone="no"?>
 <epp xmlns="urn:ietf:params:xml:ns:epp-1.0">
   <hello/>
 </epp>'''.encode("utf-8")

def generate_hosts(ns : list) -> str:
    if not ns: return ""
    result = "<domain:ns>\n"

    for serv in ns:
        if type(serv) == str:
            result += f'{f"<domain:hostObj>{serv}</domain:hostObj>"}'
        elif type(serv) == tuple:
            result += "<domain:hostAttr>\n"
            result += f"<domain:hostName>{serv[0]}</domain:hostName>\n"
            for v, adr in serv[1].items():
                result += f'<domain:hostAddr ip="{v}">{adr}</domain:hostAddr>\n'
            result += "</domain:hostAttr>\n"

    result += "</domain:ns>"
    return result

def domain_info(domain: str):
    return f'''<?xml version="1.0" encoding="UTF-8" standalone="no"?>
    <epp xmlns="urn:ietf:params:xml:ns:epp-1.0">
      <command>
        <info>
          <domain:info xmlns:domain="http://hostmaster.ua/epp/domain-1.1">
            <domain:name>{domain}</domain:name>
          </domain:info>
        </info>
      </command>
    </epp>'''.encode("utf-8")

def domain_create(name : str, period : int, ns, registrant : str, contacts : list[tuple[str, str]])-> bytes:
    return f'''<?xml version="1.0" encoding="UTF-8" standalone="no"?>
  <epp xmlns="urn:ietf:params:xml:ns:epp-1.0">
    <command>
      <create>
        <domain:create xmlns:domain="http://hostmaster.ua/epp/domain-1.1">
          <domain:name>{name}</domain:name>
          <domain:period unit="y">{period}</domain:period>
            {generate_hosts(ns)}
          <domain:registrant>{registrant}</domain:registrant>
          {"\n".join(f'<domain:contact type="{type_}">{text}</domain:contact>' for type_, text in contacts)}
        </domain:create>
      </create>
    </command>
  </epp>'''.encode("utf-8")

def host_check(hosts):
    return f'''<?xml version="1.0" encoding="UTF-8" standalone="no"?>
 <epp xmlns="urn:ietf:params:xml:ns:epp-1.0">
   <command>
     <check>
       <host:check xmlns:host="http://hostmaster.ua/epp/host-1.1">
         {"\n".join(f"<host:name>{host}</host:name>" for host in hosts) }
       </host:check>
     </check>
   </command>
</epp>
'''.encode("utf-8")

def contact_info(contact):
    return f'''<?xml version="1.0" encoding="UTF-8" standalone="no"?>
 <epp xmlns="urn:ietf:params:xml:ns:epp-1.0">
   <command>
     <info>
       <contact:info xmlns:contact="http://hostmaster.ua/epp/contact-1.1">
         <contact:id>{contact}</contact:id>
       </contact:info>
     </info>
   </command>
 </epp>
'''.encode("utf-8")


def host_create(name,ipv4,ipv6):
    return f'''<?xml version="1.0" encoding="UTF-8" standalone="no"?>
 <epp xmlns="urn:ietf:params:xml:ns:epp-1.0">
   <command>
     <create>
       <host:create xmlns:host="http://hostmaster.ua/epp/host-1.1">
         <host:name>{name}</host:name>
           {f"<host:addr ip='v4'>{ipv4}</host:addr>" if ipv4 else ""}
           {f"<host:addr ip='v6'>{ipv6}</host:addr>" if ipv6 else ""}
       </host:create>
     </create>
   </command>
 </epp>'''.encode("utf-8")


def contact_create(contact_id, name, city, country_code, email, password):
    return f'''<?xml version="1.0" encoding="UTF-8" standalone="no"?>
<epp xmlns="urn:ietf:params:xml:ns:epp-1.0">
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
  </command>
</epp>'''.encode("utf-8")
