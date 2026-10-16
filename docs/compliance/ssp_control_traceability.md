# CMMC Level 2 System Security Plan (SSP) & Control Traceability Matrix
**Organization:** Emerging Defense Solutions (EDS-360)  
**System Name:** EDS-360 Sovereign 4-Node Enclave  
**Domain Authority:** `eds-360.com`  
**Compliance Target:** CMMC Level 2 (NIST SP 800-171 R2) / FedRAMP High / JSIG  

---

## 1. System Identification & Boundary Definition

The EDS-360 Enclave is a sovereign, 4-node isolated cluster engineered to process, store, and transmit Controlled Unclassified Information (CUI).

| Node Identifier | IP Address | Host System Marking Tag | Core Functional Responsibility |
| :--- | :--- | :--- | :--- |
| **`vm-node0`** | `10.0.10.128` | `SYS-EDS-360-N0` `[CUI BOUNDARY - CONTROL PLANE]` | AI Orchestration, CMMC Pipeline Execution, POAM Engine |
| **`vm-node1`** | `10.0.10.129` | `SYS-EDS-360-N1` `[CUI BOUNDARY - PUBLIC INGRESS]` | WAF, Reverse Proxy, Edge Portal Entry, TLS Termination |
| **`vm-node2`** | `10.0.10.130` | `SYS-EDS-360-N2` `[CUI PROCESSING NODE]` | AI Core Processing, Auth Gateway, RBAC Tier Engine |
| **`vm-node3`** | `10.0.10.131` | `SYS-EDS-360-N3` `[CUI ARCHIVE & VAULT STORAGE]` | FIPS Storage, SIEM AU-2 Vault, BOE Evidence Archive |
| **`vm-node4`** | `10.0.10.132` | `SYS-EDS-360-N4` `[COMPLIANCE ACCESS POINT]` | Governance Portal, Self-Assessment Dashboard |

---

## 2. NIST SP 800-171 R2 Control Family Traceability Matrix

### Access Control (AC)
* **AC.L2-3.1.1 (Enclave Boundary Isolation):** Network perimeter enforced via Node 1 Ingress proxy and `10.0.10.0/24` subnet filtering.
* **AC.L2-3.1.2 (Role-Based Access Control):** Authenticated access restricted to verified `eds-360.com` domain accounts.
* **AC.L2-3.1.11 (Session Lock):** Mandatory 15-minute idle session auto-lock configured across all Linux host terminals.

### Audit & Accountability (AU)
* **AU.L2-3.3.1 (System Audit Event Logging):** Real-time event capture enabled across OS, auth gateways, and web services.
* **AU.L2-3.3.2 (JSIG AU-2 Audit Integration):** Automated log aggregation via `scripts/siem_au2_dashboard.py` streaming JSON reports over FIPS SSH to Node 3 Vault (`/root/vault/siem_au2_reports/`).

### Identification & Authentication (IA)
* **IA.L2-3.5.2 (FIPS Hardware Tokens):** FIPS 140-3 hardware-backed keys used for administrative transport and authentication.
* **IA.L2-3.5.3 (Multi-Factor Authentication):** YubiKey 5 Series FIPS tokens enforced via PAM (`pam_u2f.so` / `pam_pkcs11.so`) and FIDO2/WebAuthn.

### Media Protection (MP)
* **MP.L2-3.8.2 (Encrypted Removable Media):** Hardware-encrypted Apricorn Aegis USB 3.0 drives used for offline CUI audit archiving (`scripts/mount_apricorn_vault.sh`).
* **MP.L2-3.8.3 (Media Marking):** Automatic generation of `CUI_MARKING_DO_NOT_REMOVE.txt` on all mounted export drives.

### Physical Protection (PE)
* **PE.L2-3.10.1 (Physical Facility Boundary):** Server rack physical security controls and host server port access restrictions.
* **PE.L2-3.10.2 (Asset Equipment Marking):** System tagging (`SYS-EDS-360-N0` through `N4`) applied across all virtual and physical components.

### Incident Response (IR)
* **IR.L2-3.6.1 (Spillage & Incident Containment):** SOAR watchdog automation (`scripts/soar_watchdog.py`) performing automated node interface isolation upon spillage detection.
