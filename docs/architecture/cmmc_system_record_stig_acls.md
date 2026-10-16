# CMMC Level 2 System Record, STIG Baseline & Domain Access Control Specification

**Document Identifier:** `EDS-SYS-REC-2026-01`  
**Security Classification:** `Controlled Unclassified Information (CUI)` / `CMMC Level 2`  
**System Designation:** `EDS-360 Sovereign Enclave`  
**Authorized Domain Boundary:** `*.eds-360.com`  
**Last Updated:** October 16, 2026  

---

## 1. System Identification & Marking Record (CMMC PE.L2-3.10.2 / MP.L2-3.8.3)

All nodes in the sovereign enclave operate under explicit physical and virtual labels to ensure complete tracking of CUI boundaries and hardware attachments:

| Hostname / Node Name | System Asset Tag | IP Address | Attachment & Location | Purpose & Data Classification |
| :--- | :--- | :--- | :--- | :--- |
| **`vm-node0`** (`Control Plane`) | `SYS-EDS-360-N0` | `10.0.10.128` | Rack ID `EDS-SRV-00` / Port 1 | AI Agent Coordinator, POAM Generator, Control Hub (`CUI Boundary`) |
| **`vm-node1`** (`Ingress Proxy`) | `SYS-EDS-360-N1` | `10.0.10.129` | Edge Router Switch / VPort 12 | Reverse Proxy, Status Display, Public Ingress (`CUI Boundary`) |
| **`vm-node2`** (`AI Core`) | `SYS-EDS-360-N2` | `10.0.10.130` | Core Compute Cluster / Port 2 | User Auth Engine, Subscription Tier Enforcement, Payment Gateway |
| **`vm-node3`** (`Vault Storage`) | `SYS-EDS-360-N3` | `10.0.10.131` | FIPS Storage Cluster / Port 3 | SIEM AU-2 Audit Repository, CMMC BOE Archives (`CUI Storage`) |
| **`vm-node4`** (`Governance`) | `SYS-EDS-360-N4` | `10.0.10.132` | Management Cluster / Port 4 | POAM Manifests, Incident Response Dashboard, Self-Assessment |
| **`Apricorn Aegis Drive`** | `MEDIA-EDS-CUI-001` | Local USB Mount | Host Server USB 3.0 Port 1A | Portable Audit Backup (`FIPS 140-2/3 Hardware Encrypted`) |

---

## 2. STIG System Hardening Baseline (DISA STIG Rules)

The enclave enforces DISA STIG guidelines across OS, network, and logging subsystems:

### 2.1 OS Hardening (RHEL/Ubuntu DISA STIG)
- **STIG-RULE-01 (FIPS Mode):** `fips=1` enabled in GRUB bootloader. All cryptographic calls restricted to FIPS 140-3 modules.
- **STIG-RULE-02 (Passwordless Root SSH Ban):** Password authentication disabled in `/etc/ssh/sshd_config` (`PasswordAuthentication no`). Access requires ECDSA-384 SSH keys.
- **STIG-RULE-03 (SELinux Enforcement):** SELinux operating in `Enforcing` mode across all nodes. Context relabeling (`restorecon -R -v /root/.ssh`) enforced.
- **STIG-RULE-04 (Partition Isolation):** Separate filesystem partitions for `/var/log`, `/tmp`, and `/root/vault/` to prevent Denial of Service via log flooding.

### 2.2 Network & Boundary STIG Rules
- **STIG-RULE-05 (TLS Baseline):** TLS 1.0/1.1 disabled on Node 1 Ingress. Only TLS 1.3 with FIPS cipher suites enabled (`ECDHE-ECDSA-AES256-GCM-SHA384`).
- **STIG-RULE-06 (Port Isolation):** Inbound traffic on Node 3 (Vault) blocked for all IPs except Node 0 (`10.0.10.128`) on port 22.

---

## 3. Strict Domain Access Control Lists (ACLs) - `eds-360.com` Only

To prevent unauthorized access and satisfy **CMMC AC.L2-3.1.1 (Access Control)**, system access is restricted strictly to verified `eds-360.com` domain members.

### 3.1 Domain Role-Based Access Control Matrix

| Role Name | Domain Group Filter | Permitted Actions | Authentication Requirement |
| :--- | :--- | :--- | :--- |
| **Enclave Administrator** | `admin-group@eds-360.com` | Full Node 0-4 Root Access, FIPS Key Management | ECDSA-384 SSH Key + Hardware Token (MFA) |
| **CISO / Security Manager** | `secops@eds-360.com` | Audit Log Review, SIEM AU-2 Ingestion, Spillages | SSO (`@eds-360.com`) + CAC/PIV Token |
| **Compliance Officer** | `compliance@eds-360.com` | POAM Manifests, CMMC Self-Assessment Reports | SSO (`@eds-360.com`) + Hardware MFA |
| **Developer / Frontend** | `devops@eds-360.com` | Status Page Inspection, Web App Deployment | SSO (`@eds-360.com`) + FIPS Tunnel |
| **Unauthorized External** | *Any non-`eds-360.com`* | **REJECTED / IMPLICIT DENY** | N/A |

### 3.2 Linux PAM & OpenSSH Access Control Rules

The following configuration is applied to `/etc/security/access.conf` across all enclave nodes:

```text
# Enforce strict domain user isolation for eds-360.com
+ : root : 10.0.10.0/24
+ : (eds-360-admins) : ALL
- : ALL : ALL
```

System SSH daemon restriction in `/etc/ssh/sshd_config`:

```text
AllowGroups eds-360-admins
AllowUsers *@eds-360.com root@10.0.10.128
AuthenticationMethods publickey
KbdInteractiveAuthentication no
PasswordAuthentication no
```

---

## 4. Hardware Encrypted Media Export Protocol (Apricorn Aegis)

In compliance with **CMMC MP.L2-3.8.2** and **MP.L2-3.8.3**:
1. Audit evidence downloads to physical media are restricted to hardware-encrypted drives (**Apricorn Aegis Padlock** or equivalent FIPS 140-2/3 Level 3 validated devices).
2. Media must be mounted locally on Node 0 at `/mnt/apricorn-media-001`.
3. Every export automatically applies the mandatory marking file `CUI_MARKING_DO_NOT_REMOVE.txt`.
