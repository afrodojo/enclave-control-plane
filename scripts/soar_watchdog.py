import smtplib
import json
import os
import glob
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Configuration
SMTP_SERVER = "smtp.protonmail.ch"
SMTP_PORT = 587
SENDER_EMAIL = "dassenseibsu@pm.me"
ADMIN_EMAIL = "dassenseibsu@pm.me"
SMTP_PASSWORD = os.environ.get("SOAR_SMTP_PASS", "")

def evaluate_soar_incident():
    # 1. Scan SIEM and UBA feeds
    siem_files = sorted(glob.glob("docs/feeds/siem_scan_*.json"), reverse=True)
    if not siem_files:
        return
    
    with open(siem_files[0], "r") as f:
        data = json.load(f)

    failed_auth = data.get("uba_metrics", {}).get("failed_auth_attempts_24h", 0)
    threat_level = data.get("threat_level", "LOW")

    # 2. Trigger Actionable SOAR Alert if Anomaly Detected or Approval Pending
    if failed_auth > 0 or threat_level != "LOW / SECURE":
        dispatch_email_alert(
            subject=f"🚨 [SOAR ALERT] Incident Detected on Node 0 Enclave ({threat_level})",
            body=f"""
SOAR WATCHDOG ALERT
-------------------
Threat Level: {threat_level}
Failed Logins (24h): {failed_auth}

Remote Management Actions:
- Approve Pending Drafts: https://hive.eds-360.com/admin.html
- Lockdown Enclave: https://hive.eds-360.com/siem-dashboard.html?action=lockdown
            """
        )

def dispatch_email_alert(subject, body):
    if not SMTP_PASSWORD:
        print("[SOAR] SMTP password not configured. Skipping remote email dispatch.")
        return

    msg = MIMEMultipart()
    msg['From'] = SENDER_EMAIL
    msg['To'] = ADMIN_EMAIL
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    try:
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(SENDER_EMAIL, SMTP_PASSWORD)
        server.send_message(msg)
        server.quit()
        print("[SOAR] Remote email alert dispatched successfully.")
    except Exception as e:
        print(f"[SOAR ERROR] Email dispatch failed: {e}")

if __name__ == "__main__":
    evaluate_soar_incident()
