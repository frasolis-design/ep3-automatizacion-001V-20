import yaml
from ncclient import manager
import xml.etree.ElementTree as ET
import datetime
import socket
import os

# 1. Imprimir Metadatos
print("=== REPORTE DE VALIDACION NETCONF ===")
print(f"Script: validacion_netconf.py")
print(f"Fecha: {datetime.datetime.now()}")
print(f"Host VM: {socket.gethostname()}")
print("=====================================\n")

# 2. Cargar variables
with open("../vars/vars_001V-20.yaml", "r") as file:
    vars_data = yaml.safe_load(file)

router_ip = vars_data['router']['ip']
username = vars_data['router']['usuario']
password = vars_data['router']['password']

# Valores esperados
exp_hostname = vars_data['cliente']['hostname']
exp_loop_ip = vars_data['router']['loopback_ip']
exp_loop_mask = vars_data['router']['loopback_mask']
exp_desc = vars_data['router']['descripcion_wan']
exp_ntp = vars_data['router']['ntp_server']

# 3. Filtro NETCONF para Cisco-IOS-XE-native
netconf_filter = '''
<filter>
  <native xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-native"/>
</filter>
'''

# 4. Conectar y obtener configuración
with manager.connect(host=router_ip, port=830, username=username, password=password, hostkey_verify=False, look_for_keys=False, allow_agent=False) as m:
    reply = m.get_config(source='running', filter=netconf_filter)
    raw_xml = reply.xml

    # Guardar XML crudo
    os.makedirs("evidencias", exist_ok=True)
    with open("evidencias/rpc_reply_raw.xml", "w") as f:
        f.write(raw_xml)

    # 5. Parsear XML y extraer valores
    # Usamos string search/regex simple para mayor robustez ante distintas versiones de IOS-XE
    import re
    
    act_hostname = re.search(r'<hostname>([^<]+)</hostname>', raw_xml)
    act_hostname = act_hostname.group(1) if act_hostname else "No encontrado"
    
    act_ntp = re.search(r'<ip-address>([^<]+)</ip-address>', raw_xml)
    act_ntp = act_ntp.group(1) if act_ntp else "No encontrado"
    
    act_loop_ip = re.search(r'<Loopback>.*?<address>([^<]+)</address>.*?<mask>([^<]+)</mask>', raw_xml, re.DOTALL)
    if act_loop_ip:
        act_mask = act_loop_ip.group(2)
        act_loop_ip = act_loop_ip.group(1)
    else:
        act_loop_ip, act_mask = "No encontrado", "No encontrado"
        
    act_desc = re.search(r'<GigabitEthernet>.*?<description>([^<]+)</description>', raw_xml, re.DOTALL)
    act_desc = act_desc.group(1) if act_desc else "No encontrado"

    # 6. Comparación y Reporte
    score = 0
    def verificar(criterio, esperado, obtenido):
        global score
        if esperado == obtenido:
            print(f"- {criterio}: Esperado '{esperado}' | Obtenido '{obtenido}' -> [OK]")
            score += 1
        else:
            print(f"- {criterio}: Esperado '{esperado}' | Obtenido '{obtenido}' -> [FAIL]")

    verificar("Hostname corporativo", exp_hostname, act_hostname)
    verificar("IP Loopback de gestion", exp_loop_ip, act_loop_ip)
    verificar("Mascara Loopback", exp_loop_mask, act_mask)
    verificar("Descripcion WAN", exp_desc, act_desc)
    verificar("Servidor NTP", exp_ntp, act_ntp)

    print("\n-------------------------------------")
    if score == 5:
        print(f"RESULTADO GLOBAL: CONFORME ({score}/5)")
    else:
        print(f"RESULTADO GLOBAL: NO CONFORME ({score}/5)")
    print("-------------------------------------")
