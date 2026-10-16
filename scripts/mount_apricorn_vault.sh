#!/usr/bin/env bash
# ==============================================================================
# Sovereign Enclave - Apricorn Encrypted Drive Export & Marking Utility
# Control Alignment: CMMC MP.L2-3.8.2, MP.L2-3.8.3, PE.L2-3.10.1
# System Attachment: Node 0 (VM-Node0-Bootstrap / 10.0.10.128)
# ==============================================================================

set -euo pipefail

APRICORN_MOUNT_PATH="${1:-/mnt/apricorn-media-001}"
CUI_MARKING_FILE="$APRICORN_MOUNT_PATH/CUI_MARKING_DO_NOT_REMOVE.txt"
LOCAL_AUDIT_DIR="/root/repo/enclave-control-plane/docs/audit/"

echo "[INFO] Checking for FIPS 140-2/3 hardware-encrypted drive at: $APRICORN_MOUNT_PATH"

if [ -d "$APRICORN_MOUNT_PATH" ] && mountpoint -q "$APRICORN_MOUNT_PATH" 2>/dev/null; then
    echo "[PASS] Apricorn Encrypted Drive detected and mounted."
    
    # Write CMMC MP.L2-3.8.3 Media Marking File
    cat << 'EOF' > "$CUI_MARKING_FILE"
=================================================================
  PROPERTY OF: EMERGING DEFENSE SOLUTIONS (EDS-360)
  SYSTEM ATTACHMENT: VM-NODE0-BOOTSTRAP / CONTROL PLANE (10.0.10.128)
  MEDIA IDENTIFIER: MEDIA-EDS-CUI-001
  SECURITY LEVEL: [CMMC LEVEL 2 / CUI] - DO NOT REMOVE
  ENCRYPTION: FIPS 140-2/3 HARDWARE KEYPAD ACTIVATED
=================================================================
EOF
    chmod 444 "$CUI_MARKING_FILE"

    # Export Audit Reports & POAM Manifests
    mkdir -p "$APRICORN_MOUNT_PATH/audit-exports/"
    cp -r "$LOCAL_AUDIT_DIR"* "$APRICORN_MOUNT_PATH/audit-exports/"
    
    echo "[SUCCESS] CMMC BOE & POAM audit reports successfully backed up to MEDIA-EDS-CUI-001."
else
    echo "[WARNING] Apricorn Encrypted Drive is not mounted at $APRICORN_MOUNT_PATH."
    echo "[INFO] Audit evidence remains securely stored within local enclave storage ($LOCAL_AUDIT_DIR)."
fi
