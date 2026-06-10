import requests
import yaml
import json
import urllib3
import datetime
import socket

# Desactivar advertencias de certificados autofirmados
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

print("=== REPORTE DE VALIDACION RESTCONF ===")
print(f"Script: validacion_restconf.py")
print(f"Fecha: {datetime.datetime.now()}")
print(f"Host VM: {socket.gethostname()}")
print("======================================\n")

# Cargar variables del alumno
with open("../vars/vars_001V-20.yaml", "r") as file:
    vars_data = yaml.safe_load(file)

ip = vars_data['router']['ip']
auth = (vars_data['router']['usuario'], vars_data['router']['password'])
headers = {"Accept": "application/yang-data+json"}
base_url = f"https://{ip}/restconf/data"

score = 0

def verificar(criterio, esperado, raw_json):
    global score
    json_str = json.dumps(raw_json)
    if esperado in json_str:
        print(f"- {criterio}: Esperado '{esperado}' | Obtenido '{esperado}' -> [OK]")
        score += 1
    else:
        print(f"- {criterio}: Esperado '{esperado}' | Obtenido 'No encontrado' -> [FAIL]")

# 1. Consultar y guardar Hostname
r1 = requests.get(f"{base_url}/Cisco-IOS-XE-native:native/hostname", auth=auth, headers=headers, verify=False)
with open("evidencias/responses/get_hostname.json", "w") as f:
    json.dump(r1.json(), f, indent=4)
verificar("Hostname corporativo", vars_data['cliente']['hostname'], r1.json())

# 2. Consultar y guardar IP Loopback
r2 = requests.get(f"{base_url}/ietf-interfaces:interfaces/interface=Loopback10", auth=auth, headers=headers, verify=False)
with open("evidencias/responses/get_loopback.json", "w") as f:
    json.dump(r2.json(), f, indent=4)
verificar("IP Loopback de gestion", vars_data['router']['loopback_ip'], r2.json())

# 3. Consultar y guardar Descripcion WAN
r3 = requests.get(f"{base_url}/ietf-interfaces:interfaces/interface=GigabitEthernet1", auth=auth, headers=headers, verify=False)
with open("evidencias/responses/get_interfaces.json", "w") as f:
    json.dump(r3.json(), f, indent=4)
verificar("Descripcion WAN", vars_data['router']['descripcion_wan'], r3.json())

# 4. Consultar y guardar Servidor NTP
r4 = requests.get(f"{base_url}/Cisco-IOS-XE-native:native/ntp", auth=auth, headers=headers, verify=False)
with open("evidencias/responses/get_ntp.json", "w") as f:
    json.dump(r4.json(), f, indent=4)
verificar("Servidor NTP", vars_data['router']['ntp_server'], r4.json())

print("\n-------------------------------------")
if score == 4:
    print(f"RESULTADO GLOBAL: CONFORME ({score}/4)")
else:
    print(f"RESULTADO GLOBAL: NO CONFORME ({score}/4)")
print("-------------------------------------")
