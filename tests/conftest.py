"""Test configuration: load .env before any metagpt import."""
import os
from pathlib import Path

# Load .env manually before metagpt imports
dotenv_path = Path(__file__).resolve().parent.parent / ".env"
if dotenv_path.exists():
    with open(dotenv_path) as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                key, _, value = line.partition("=")
                os.environ.setdefault(key.strip(), value.strip())

# Ensure required env vars are set (even if .env is missing)
os.environ.setdefault("LLM_PROVIDER", "openai")
os.environ.setdefault("OPENAI_BASE_URL", "http://localhost:13000/v1")
os.environ.setdefault("OPENAI_API_MODEL", "deepseek-ai/deepseek-v4-flash")
os.environ.setdefault("TIMEOUT", "180")