from XMLGenerator import wrap_in_epp_element, build_hosts, build_contacts, build_add, build_rem, build_chg
from config import NAMESPACES


def domain_create_no_registrant(name : str, period : int, ns:list[str|tuple[str,dict[str:str]]], contacts : list[tuple[str, str]]) -> str:
    return wrap_in_epp_element(f'''
    <command>
      <create>
        <domain:create xmlns:domain="{NAMESPACES["domain"]}">
          <domain:name>{name}</domain:name>
          <domain:period unit="y">{period}</domain:period>
            {build_hosts(ns)}
          {build_contacts(contacts)}
        </domain:create>
      </create>
    </command>''')

def domain_update_without_domain_name(add:dict[str:list],rem:dict[str:list],chg:dict[str:list]) -> str:
    return wrap_in_epp_element(f'''
    <command>
      <update>
        <domain:update
         xmlns:domain="{NAMESPACES["domain"]}">
          {build_add(add)}
          {build_rem(rem)}
          {build_chg(chg)}
        </domain:update>
      </update>
    </command>''')

def domain_restore_without_domain_name():
    return wrap_in_epp_element(f'''
    <command>
      <update>
        <domain:update
         xmlns:domain="{NAMESPACES["domain"]}">
        </domain:update>
      </update>
      <extension>
        <rgp:update
         xmlns:rgp="{NAMESPACES["rgp"]}">
          <rgp:restore op="request"/>
        </rgp:update>
      </extension>
    </command>''')


def domain_restore_with_change_block(name):
    return wrap_in_epp_element(f'''
    <command>
      <update>
        <domain:update
         xmlns:domain="{NAMESPACES["domain"]}">
          <domain:name>{name}</domain:name>
          <domain:chg>
          <domain:registrant>123</domain:registrant>
          </domain:chg>
        </domain:update>
      </update>
      <extension>
        <rgp:update
         xmlns:rgp="{NAMESPACES["rgp"]}">
          <rgp:restore op="request"/>
        </rgp:update>
      </extension>
    </command>''')

def host_info_without_host_name() -> str:
    return wrap_in_epp_element(f'''
    <command>
     <info>
       <host:info xmlns:host="{NAMESPACES["host"]}">
       </host:info>
     </info>
   </command>''')

def host_create_without_host_name(ipv4:str,ipv6:str) -> str:
    return wrap_in_epp_element(f'''
    <command>
     <create>
       <host:create xmlns:host="{NAMESPACES["host"]}">
           {f"<host:addr ip='v4'>{ipv4}</host:addr>" if ipv4 else ""}
           {f"<host:addr ip='v6'>{ipv6}</host:addr>" if ipv6 else ""}
       </host:create>
     </create>
   </command>''')

def host_delete_without_host_name() -> str:
    return wrap_in_epp_element(f'''
    <command>
      <delete>
        <host:delete xmlns:host="{NAMESPACES["host"]}">
        </host:delete>
      </delete>
    </command>''')