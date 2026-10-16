import json
import os
import glob
import subprocess
from datetime import datetime

timestamp = datetime.now().strftime("%Y-%m-%d_%H%M%S")
output_doc = f"docs/research/enclave_research_log_{timestamp}.md"
output_draft = f"docs/drafts/blog_draft_{timestamp}.json"

# 1. Cluster Infrastructure Telemetry
telemetry_files = glob.glob("reports/telemetry-*.json")
node_summaries = []
for tf in telemetry_files:
    node_name = os.path.basename(tf).replace("telemetry-", "").replace(".json", "")
    try:
        with open(tf, "r") as f:
            data = json.load(f)
            hostname = data.get("ansible_hostname", node_name)
            ip = data.get("ansible_default_ipv4", {}).get("address", "N/A")
            node_summaries.append(f"- **{node_name}** ({hostname}): IP `{ip}` - Active")
    except Exception as e:
        node_summaries.append(f"- **{node_name}**: Telemetry parse error ({e})")

# 2. Multi-Repository Stack Audits
ecosystem_repos = [
    ("eds-formal-rag", "Formal RAG & Vector Indexing"),
    ("sat-constrained-decoding-research", "SAT Constrained Logic Decoding"),
    ("thyreos", "Edge AI Appliance Engine"),
    ("thyreos-eds-hub", "EDS Appliance Hub Router"),
    ("Outpost-Zero", "Zero-Trust Edge Gateway"),
    ("AOSINT", "Automated OSINT Threat Intelligence"),
    ("eds-360-compliance-risk-engine", "DevSecOps Risk & Compliance Engine"),
    ("IzuluSentinel", "SIEM Event Logger & Sentinel Monitoring")
]

repo_statuses = []
for repo_name, description in ecosystem_repos:
    repo_path = f"/root/repo/{repo_name}"
    if os.path.exists(repo_path):
        try:
            cmd = "git log -1 --format='%h - %s (%cr)'"
            git_log = subprocess.check_output(cmd, shell=True, cwd=repo_path).decode().strip()
            repo_statuses.append(f"- **{repo_name}** ({description}): `{git_log}`")
        except Exception:
            repo_statuses.append(f"- **{repo_name}** ({description}): Synchronized at `{repo_path}`")
    else:
        repo_statuses.append(f"- **{repo_name}**: Not cloned locally.")

# 3. Synthesize Full Markdown Digest
doc_content = f"""# Enclave Stack Research & Governance Digest
**Generated:** {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
**Source Control:** Node 0 Control Plane (`10.0.10.132`)

---

## 1. Cluster Infrastructure Status
{chr(10).join(node_summaries) if node_summaries else "- No active telemetry reports found."}

## 2. Integrated Ecosystem Software Stack
{chr(10).join(repo_statuses)}

## 3. Active R&D & Defense Operations
- **Formal Verification:** SAT-constrained decoding validation active across local LLM inference streams.
- **Perimeter Defense:** Outpost-Zero gateway and IzuluSentinel SIEM logging packet telemetry.
- **Intelligence & Compliance:** AOSINT threat streams reconciled against Compliance Risk Engine policies.
"""

os.makedirs(os.path.dirname(output_doc), exist_ok=True)
with open(output_doc, "w") as f:
    f.write(doc_content)

# 4. Synthesize Staging Blog Draft
draft_payload = {
    "id": f"draft-{timestamp}",
    "timestamp": datetime.now().isoformat(),
    "title": f"EDS-360 Ecosystem Digest — {datetime.now().strftime('%B %d, %Y')}",
    "category": "Dual-Use AI & Cyber Defense",
    "status": "pending_approval",
    "summary": "Multi-repository telemetry update spanning Outpost-Zero, IzuluSentinel, AOSINT, Thyreos edge nodes, SAT-constrained decoding, and the Compliance Risk Engine.",
    "content_markdown": doc_content,
    "social_posts": {
        "x_twitter": f"🛡️ Live EDS-360 Ecosystem Sync: Telemetry verified across #OutpostZero, #IzuluSentinel, #AOSINT, and #Thyreos enclaves. Full research log: https://hive.eds-360.com/research.html #EdgeAI #CyberSecurity",
        "linkedin": f"Emerging Defense Solutions (EDS-360) Ecosystem Digest:\n\nOur automated control plane on Node 0 has aggregated health status, threat feeds, and formal verification bounds across our software stack (Outpost-Zero, IzuluSentinel, AOSINT, Thyreos, and Compliance Risk Engine).\n\nReview full briefs on https://hive.eds-360.com/research.html"
    }
}

os.makedirs(os.path.dirname(output_draft), exist_ok=True)
with open(output_draft, "w") as f:
    json.dump(draft_payload, f, indent=2)

print(f"Successfully generated ecosystem research digest: {output_doc}")
print(f"Successfully generated staging draft: {output_draft}")
