#!/usr/bin/env python3
import os
import subprocess

# snapshot_download no longer needed; using model id directly

MODEL_ID = "openai/gpt-oss-120b"
REVISION = "main"

# Environment (prefer HF_HUB_OFFLINE for strict offline if desired)
env = os.environ.copy()
# Set to "1" only if you want zero network calls. Leave unset to allow refresh of 'main'.
env["HF_HUB_OFFLINE"] = "1"

# Allow overriding host, port, and optional API key via environment variables.
# Defaults: HOST=0.0.0.0, PORT=8000. If VLM_API_KEY is set (non-empty), we pass
# it through as an --api-key enforcing auth; if unset or empty we do not add the flag.
HOST = os.environ.get("HOST", "0.0.0.0")
PORT = os.environ.get("PORT", "8000")
VLM_API_KEY = os.environ.get("VLM_API_KEY", "").strip()

cmd = [
    "vllm",
    "serve",
    MODEL_ID,
    "--revision",
    REVISION,
    "--served-model-name",
    "gpt-oss-120b",
    "--enable-auto-tool-choice",
    "--tool-call-parser",
    "openai",
    "--host",
    HOST,
    "--port",
    PORT,
]

if VLM_API_KEY:
    # Accept comma-separated keys if provided; split and append each.
    # This mirrors vLLM's support for multiple keys after --api-key.
    cmd.append("--api-key")
    # Keep original string if multiple keys separated by commas
    if "," in VLM_API_KEY:
        cmd.extend([k.strip() for k in VLM_API_KEY.split(",") if k.strip()])
    else:
        cmd.append(VLM_API_KEY)

subprocess.run(cmd, check=True, env=env)
