# FedRAMP Incident Response Playbook & Data Spillage Protocol

**Document Identifier:** IR-PLAYBOOK-EDS-360-001  
**Target Accreditation:** CMMC Level 2 (NIST SP 800-171 R2) / FedRAMP High / JSIG  
**Control Mapping:** CMMC IR.L2-3.6.1, IR.L2-3.6.2, IR.L2-3.6.3 / NIST SP 800-53 IR Family  
**Organization:** Emerging Defense Solutions (EDS-360)  
**Sovereign Domain Authority:** `eds-360.com`  
**Classification:** Controlled Unclassified Information (CUI) / Incident Response Record  

---

## 1. Purpose & Scope

This Standard Operating Playbook establishes the mandatory operational protocol for detecting, containing, analyzing, sanitizing, and reporting security incidents and Controlled Unclassified Information (CUI) data spillages within the **EDS-360 Sovereign 4-Node Enclave** (`vm-node0` through `vm-node4`).

This playbook applies to all human personnel, automated system agents, network traffic boundaries, and physical hardware assets assigned to the `eds-360.com` domain.

---

## 2. Enclave Incident Response Roles & Contact Roster

| Role | Operational Responsibility | Contact Email / Interface | Authority Level |
| :--- | :--- | :--- | :--- |
| **Chief Information Security Officer (CISO)** | Incident Commander, Containment Approval, Assessor Notification | `ciso@eds-360.com` | Final Decision Authority |
| **Security Manager / Incident Lead** | Technical Investigation, Evidence Packaging, POAM Updates | `security@eds-360.com` | Triage & Analysis Lead |
| **Lead Infrastructure Engineer** | Network Isolation, SSH Tunnel Lockout, Firewall Rule Adjustments | `sysadmin@eds-360.com` | Technical Containment Executer |
| **Automated SOAR Agent** | Real-Time Telemetry Scanning, Log Hash Preservation, Port Isolation | `scripts/soar_watchdog.py` | Automated Response Engine |
| **Vault Audit Logger** | Immutable Log Vault & SHA-384 Evidence Archive | `vm-node3 (10.0.10.131)` | Forensic Log Repository |

---

## 3. Incident Lifecycle & Containment Workflow

┌─────────────────────────────────────────────────────────────────────────┐
│                          PHASE 1: DETECTION                             │
│       • Telemetry Anomaly Detection via soar_watchdog.py               │
│       • SIEM AU-2 Audit Alerting / Failed Authentication Spikes        │
└────────────────────────────────────┬────────────────────────────────────┘
│
▼
┌─────────────────────────────────────────────────────────────────────────┐
│                         PHASE 2: CONTAINMENT                            │
│       • Automated Node Isolation on Node 1 Ingress Proxy                │
│       • Termination of Non-eds-360.com Sessions                        │
│       • FIPS SSH Transport Lockout to Read-Only Mode                    │
└────────────────────────────────────┬────────────────────────────────────┘
│
▼
┌─────────────────────────────────────────────────────────────────────────┐
│                    PHASE 3: EVIDENCE PRESERVATION                       │
│       • Execution of siem_au2_dashboard.py Snapshot                     │
│       • SHA-384 Log Hashing & Transfer to Node 3 Vault                 │
└────────────────────────────────────┬────────────────────────────────────┘
│
▼
┌─────────────────────────────────────────────────────────────────────────┐
│                     PHASE 4: MEDIA SANITIZATION                         │
│       • Data Spillage Purge per NIST SP 800-88 Rev. 1 Guidelines        │
│       • Apricorn Aegis Drive Overwrite / Physical Key Erasure           │
└────────────────────────────────────┬────────────────────────────────────┘
│
▼
┌─────────────────────────────────────────────────────────────────────────┐
│                   PHASE 5: NOTIFICATION & REPORTING                     │
│       • CISO Briefing within 1 Hour of Confirmation                     │
│       • Formal DoD DC3 / FedRAMP PMO / 3PAO Report within 24 Hours      │
└─────────────────────────────────────────────────────────────────────────┘


---

## 4. Detailed Incident Response Phases

### Phase 1: Detection & Threat Identification
1. **Automated Monitoring:** The Security Operations Automated Response agent (`scripts/soar_watchdog.py`) runs continuously on **Node 0 (`10.0.10.128`)**, monitoring syslog feeds, SSH authentication logs (`/var/log/secure`), and WAF ingress traffic.
2. **Trigger Indicators:**
   * Multiple failed SSH authentication attempts originating outside the `10.0.10.0/24` subnet.
   * Access attempts using non-`eds-360.com` commit signatures or unauthorized PIV key handles.
   * CUI data pattern detected on unauthorized public endpoints (`vm-node1`).
3. **Alert Escalation:** Automated generation of an alert file written to `/root/vault/siem_au2_reports/` on **Node 3 (`10.0.10.131`)**.

### Phase 2: Immediate Containment Protocol
1. **Network Boundary Lockdown:**
   * **Node 1 (`Ingress`):** Drop all inbound external connections on port 443 and port 22 except from whitelisted CISO administrative IPs.
   * **Node 2 (`AI Core`):** Revoke all active API tokens and authentication sessions immediately.
2. **User Session Termination:** Force-kill active shell sessions for unverified users:
   ```bash
   pkill -kill -u <unauthorized_user>
Repository Lockout: Set local Git repositories to read-only state to prevent unauthorized code pushes during investigation.

Phase 3: Evidence Preservation & Forensic Packaging
Log Snapshot: Execute the SIEM log aggregation suite on Node 0:

Bash
python3 scripts/siem_au2_dashboard.py
Cryptographic Checksum Verification: Generate SHA-384 hashes for all system logs and store the hash manifest on Node 3 Vault:

Bash
sha384sum /var/log/secure /var/log/messages > /tmp/incident_log_hashes.sha384
scp -i /root/.ssh/id_ecdsa /tmp/incident_log_hashes.sha384 root@10.0.10.131:/root/vault/siem_au2_reports/
Chain of Custody: Document log timestamps, system memory dumps, and physical asset state in the POAM Governance log (scripts/fedramp_poam_governance.py).

Phase 4: Data Spillage Protocol & Sanitization (IR.L2-3.6.1)
In the event that Classified Information or unauthorized CUI is spilled onto unapproved enclave nodes or portable media:

Isolation: Disconnect the affected node or drive immediately. Do not power off virtual machines to preserve volatile memory evidence.

Sanitization Standard: Perform media sanitization in strict accordance with NIST SP 800-88 Rev. 1 Guidelines for Media Sanitization:

Virtual Disk / Volume Clear: Overwrite affected volume space with pattern passes using dd or shred.

Apricorn Encrypted Drive (MEDIA-EDS-CUI-001): Execute hardware keypad admin reset (KEY + 7 + 0 force erase) to purge encryption keys, rendering data completely irrecoverable.

Sanitization Certification: Document sanitization completion date, system serial numbers, and performing engineer signature in docs/audit/.

Phase 5: Incident Reporting & Federal Notifications
Internal Notification: CISO (ciso@eds-360.com) must be verbally and electronically briefed within 1 hour of incident confirmation.

External Notification Deadlines:

DoD Cyber Crime Center (DC3): Report within 72 hours of confirmation via https://dibnet.dod.mil per DFARS 252.204-7012.

FedRAMP PMO / US-CERT: Report within 1 hour for High-severity incidents per FedRAMP Incident Communications Procedure.

CMMC 3PAO Assessor: Submit formal incident log prior to accreditation sign-off.

5. Post-Incident Review & Lessons Learned
Within 5 business days following incident resolution:

Conduct a mandatory Lessons Learned meeting with CISO, Lead Engineer, and Compliance Lead.

Update system firewall rules, DISA STIG baselines, and YubiKey access lists based on root cause findings.

Log any residual control gaps into the official POAM manifest via scripts/fedramp_poam_governance.py.
