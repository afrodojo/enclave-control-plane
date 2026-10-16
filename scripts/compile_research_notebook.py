import json
import os
import glob
from datetime import datetime

timestamp = datetime.now().strftime('%Y-%m-%d_%H%M%S")
output_doc = f"docs/research/enclave_research_log_{timestamp}.md"

telemetry_files = glob.glob("reports/telemetry-*.json")
node_summaries = []

for tf in telemetry_files:
    node_name = os.path.basename(tf).replace("telemetry-", "").replace(".json",
    try:
       with open(tf, "r") as f:
            data = json.load(f)
            hostname = data.get("ansible_hostname", node_name)
            ip = data.get("ansible_default_ipv4", {}).get("address", "N/A")
            node_summaries.append(f"- **{node_name}** ({hostnam}): IP `{ip}` -
    except Exception as e:
       node_summaries.append(f"- **{node_name}**: Telemetry parse error ({e})")
doc_content = f"""# Enclave Research & Architecture Digest
**Generated:** {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
**Source Control:** Node 0 Control Plane (`10.0.10.132`)

---

## 1. Cluster Infrastructure Status
{chr(10).join(node_summaries) if node_summaries else "- No recent telemetry reoorts found."}

## 2. Research & Fine-Tuning Environment
- **Model Target:** Llama 3.1 8B (`llama3.1:8b`) on Node 2 (`10.0.10.130`)
- **Secrets Management:** Custom HTTP Vault Service on Node 3 (`10.0.10.131:8200`).
- **Governance & Audit:** Packet Listener on Node 4 (`10.0.10.x:8081`).
- **Security Perimeter:** Subnet isolation on `VMnet` with reverse-proxy Bearertoken validation.

## 3. Active R&D Hypotheses & Experiments
cat << 'EOF' > scripts/compile_research_notebook.py
import json
import os
import glob
from datetime import datetime

timestamp = datetime.now().strftime('%Y-%m-%d_%H%M%S")
output_doc = f"docs/research/enclave_research_log_{timestamp}.md"

telemetry_files = glob.glob("reports/telemetry-*.json")
node_summaries = []

for tf in telemetry_files:
    node_name = os.path.basename(tf).replace("telemetry-", "").replace(".json",
    try:
       with open(tf, "r") as f:
            data = json.load(f)
            hostname = data.get("ansible_hostname", node_name)
            ip = data.get("ansible_default_ipv4", {}).get("address", "N/A")
            node_summaries.append(f"- **{node_name}** ({hostnam}): IP `{ip}` -
    except Exception as e:
       node_summaries.append(f"- **{node_name}**: Telemetry parse error ({e})")
doc_content = f"""# Enclave Research & Architecture Digest
**Generated:** {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
**Source Control:** Node 0 Control Plane (`10.0.10.132`)

---

## 1. Cluster Infrastructure Status
{chr(10).join(node_summaries) if node_summaries else "- No recent telemetry reoorts found."}

## 2. Research & Fine-Tuning Environment
- **Model Target:** Llama 3.1 8B (`llama3.1:8b`) on Node 2 (`10.0.10.130`)
- **Secrets Management:** Custom HTTP Vault Service on Node 3 (`10.0.10.131:8200`).
- **Governance & Audit:** Packet Listener on Node 4 (`10.0.10.x:8081`).
- **Security Perimeter:** Subnet isolation on `VMnet` with reverse-proxy Bearertoken validation.

## 3. Active R&D Hypotheses & Experiments
- **Quantization & Throughput:** Benchmarking stream output latency across isolated L3 interfaces.
- **Automated Telemetry Pipeline:** Aggregating node facts via Ansible into structured Markdown digests.
"""

os.makedirs(os.path.dirname(output_doc), exist_ok=True)
with open(output_doc, "w") as f:
    f.write(doc_content)

print(f"Successfully generated research digest: {output_doc}")
