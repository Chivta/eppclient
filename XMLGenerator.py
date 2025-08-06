# XML templates for requests
from config import NAMESPACES

def wrap_in_epp_element(content: str) -> str:
    return f'''<?xml version="1.0" encoding="UTF-8" standalone="no"?>
 <epp xmlns="{NAMESPACES["epp"]}">
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
        <objURI>{NAMESPACES["contact"]}</objURI>
        <objURI>{NAMESPACES["domain"]}</objURI>
        <objURI>{NAMESPACES["host"]}</objURI>
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
       <domain:check xmlns:domain="{NAMESPACES["domain"]}">
         {"".join(f"<domain:name>{domain}</domain:name>" for domain in domains)}
       </domain:check>
     </check>
   </command>''')

def hello() -> str:
    return wrap_in_epp_element('''
   <hello/>''')

def build_hosts(ns : list[str|tuple[str,dict[str:str]]]) -> str:
    if not ns: return ""
    result = "<domain:ns>\n"

    for serv in ns:
        if type(serv) == str:
            result += f'{f"<domain:hostObj>{serv}</domain:hostObj>"}'
        elif type(serv) == tuple:
            result += "<domain:hostAttr>\n"
            if host_name:= serv[0]:
                result += f"<domain:hostName>{host_name}</domain:hostName>\n"

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
          <domain:info xmlns:domain="{NAMESPACES["domain"]}">
            <domain:name>{domain}</domain:name>
          </domain:info>
        </info>
    </command>''')

def domain_create(name : str, period : int, ns:list[str|tuple[str,dict[str:str]]], registrant : str, contacts : list[tuple[str, str]]) -> str:
    return wrap_in_epp_element(f'''
    <command>
      <create>
        <domain:create xmlns:domain="{NAMESPACES["domain"]}">
          <domain:name>{name}</domain:name>
          <domain:period unit="y">{period}</domain:period>
            {build_hosts(ns)}
          <domain:registrant>{registrant}</domain:registrant>
          {build_contacts(contacts)}
        </domain:create>
      </create>
    </command>''')

def build_contacts(contacts : list[tuple[str, str]]):
    return "\n".join(f'<domain:contact type="{type_}">{text}</domain:contact>' for type_, text in contacts)

def host_check(hosts) -> str:
    return wrap_in_epp_element(f'''
   <command>
     <check>
       <host:check xmlns:host="{NAMESPACES["host"]}">
         {"\n".join(f"<host:name>{host}</host:name>" for host in hosts) }
       </host:check>
     </check>
   </command>''')

def host_delete(name:str) -> str:
    return wrap_in_epp_element(f'''
    <command>
      <delete>
        <host:delete xmlns:host="{NAMESPACES["host"]}">
          <host:name>{name}</host:name>
        </host:delete>
      </delete>
    </command>''')

def contact_info(contact) -> str:
    return wrap_in_epp_element(f'''
   <command>
     <info>
       <contact:info xmlns:contact="{NAMESPACES["contact"]}">
         <contact:id>{contact}</contact:id>
       </contact:info>
     </info>
   </command>''')


def host_create(name:str,ipv4:str,ipv6:str) -> str:
    return wrap_in_epp_element(f'''
    <command>
     <create>
       <host:create xmlns:host="{NAMESPACES["host"]}">
         <host:name>{name}</host:name>
           {f"<host:addr ip='v4'>{ipv4}</host:addr>" if ipv4 else ""}
           {f"<host:addr ip='v6'>{ipv6}</host:addr>" if ipv6 else ""}
       </host:create>
     </create>
   </command>''')


def contact_build_post_info(name, city, cc):
    return f'''
    <contact:postalInfo type="int">
      {f"<contact:name>{name}</contact:name>" if name else ""}
      {f"""<contact:addr>
        {f"<contact:city>{city}</contact:city>" if city else ""}
        {f"<contact:cc>{cc}</contact:cc>" if cc else ""}
      </contact:addr>""" if city or cc else ""}
    </contact:postalInfo>''' if name or city or cc else ""


def contact_create(contact_id, name, city, country_code, email, password) -> str:
    return wrap_in_epp_element(f'''
    <command>
        <create>
          <contact:create xmlns:contact="{NAMESPACES["contact"]}">
            <contact:id>{contact_id}</contact:id>
            {contact_build_post_info(name,city,country_code)}
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
        <domain:delete xmlns:domain="{NAMESPACES["domain"]}">
          <domain:name>{domain}</domain:name>
        </domain:delete>
      </delete>
    </command>''')


def contact_delete(contact_id:str) -> str:
    return wrap_in_epp_element(f'''
    <command>
      <delete>
        <contact:delete xmlns:contact="{NAMESPACES["contact"]}">
          <contact:id>{contact_id}</contact:id>
        </contact:delete>
      </delete>
    </command>''')

def contact_check(contact_ids:list[str]) -> str:
    return wrap_in_epp_element(f'''
    <command>
     <check>
       <contact:check xmlns:contact="{NAMESPACES["contact"]}">
        {"".join(f"<contact:id>{contact_id}</contact:id>" for contact_id in contact_ids)}
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

def host_update(name, add, rem: dict):
    return wrap_in_epp_element(f'''
   <command>
     <update>
       <host:update xmlns:host="{NAMESPACES["host"]}">
         <host:name>{name}</host:name>
         {f"""<host:add>
           {"\n".join([f'<host:addr ip="{v}">{adr}</host:addr>' for v, adr in add["ip"].items() if adr])}
         </host:add>""" if add["ip"] else ""}
         {f"""<host:rem>
           {"\n".join([f'<host:addr ip="{v}">{adr}</host:addr>' for v, adr in rem["ip"].items() if adr])}
         </host:rem>""" if rem.get("ip") else ""}
       </host:update>
     </update>
   </command>''')


def domain_renew(name: str, cur_exp_date: str, period: int) -> str:
    return wrap_in_epp_element(f'''
    <command>
      <renew>
        <domain:renew xmlns:domain="{NAMESPACES["domain"]}">
          <domain:name>{name}</domain:name>
          <domain:curExpDate>{cur_exp_date}</domain:curExpDate>
          <domain:period unit="y">{period}</domain:period>
        </domain:renew>
      </renew>
    </command>
''')

def build_add(add:dict[str:list]):
    return f'''
    <domain:add>
        {build_hosts(add.get("hosts"))}
        {build_contacts(add.get("contacts"))}
    </domain:add>''' if add else ""

def build_rem(rem:dict[str:list]):
    return f'''
    <domain:add>
        {build_hosts(rem["hosts"])}
        {build_contacts(rem["contacts"])}
    </domain:add>''' if rem else ""

def build_chg(chg:dict[str:list]):
    return f'''
    <domain:chg>
          <domain:registrant>{chg["registrant"]}</domain:registrant>
    </domain:chg>''' if chg else ""

def domain_update(domain: str, add:dict[str:list],rem:dict[str:list],chg:dict[str:list]) -> str:
    return wrap_in_epp_element(f'''
    <command>
      <update>
        <domain:update
         xmlns:domain="{NAMESPACES["domain"]}">
          <domain:name>{domain}</domain:name>
          {build_add(add)}
          {build_rem(rem)}
          {build_chg(chg)}
        </domain:update>
      </update>
    </command>''')

def build_contact_chg(name,city,cc,email,password):
    return f'''
    <contact:chg>
       {contact_build_post_info(name,city,cc)}
        {f"<contact:email>{email}</contact:email>" if email else ""}
        {f"""<contact:authInfo>
          <contact:pw>{password}</contact:pw>
        </contact:authInfo>""" if password else ""}  
    </contact:chg>'''

def contact_update(contact_id, add, rem, chg):
    return wrap_in_epp_element(f'''<command>
     <update>
       <contact:update xmlns:contact="{NAMESPACES["contact"]}">
         <contact:id>{contact_id}</contact:id>
         {build_contact_chg(chg.get("name"),chg.get("city"),chg.get("cc"),chg.get("email"),chg.get("password"))}
       </contact:update>
     </update>
   </command>''')