# Proyecto: Automatización de Infraestructura de Red (EP3)

Este repositorio contiene la evidencia técnica y los scripts desarrollados para la automatización, validación y auditoría de un router Cisco CSR1kv utilizando herramientas de la suite Cisco DevNet.

## Estructura del Proyecto

El laboratorio se dividió en 5 fases críticas de automatización:

- **Fase 1: Baseline (Estado Inicial)**
  - Captura del estado operativo inicial (Interfaces, Plataforma y Routing) mediante `pyATS` y `Genie`.
- **Fase 2: Aprovisionamiento (Ansible)**
  - Implementación de configuraciones corporativas, cambio de hostname a `RTR-SERREM`, y configuración de seguridad mediante Playbooks de Ansible.
- **Fase 3: Validación NETCONF**
  - Verificación de la conectividad programable y validación de parámetros de red utilizando protocolos NETCONF.
- **Fase 4: Validación RESTCONF**
  - Implementación de scripts Python para consulta y validación de estado vía APIs RESTCONF.
- **Fase 5: Auditoría de Cumplimiento (Compliance)**
  - Auditoría final mediante `genie diff` para comparar el estado post-configuración vs el baseline inicial.

## Stack Tecnológico

* **OS:** Linux (Debian/Ubuntu)
* **Red:** Cisco IOS-XE (CSR1kv)
* **Automatización:** Ansible
* **Validación:** pyATS, Genie, Python (Netmiko, Requests)
* **Control de Versiones:** Git / GitHub

## Autor
**Francisco Solis Garrido** - Estudiante de Ingeniería en Conectividad y Redes - Duoc UC.

---
*Este proyecto demuestra la capacidad de gestionar el ciclo de vida de un dispositivo de red mediante código (Infrastructure as Code).*
