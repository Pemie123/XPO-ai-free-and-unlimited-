"""
scripts/pollinations_setup.py

Helper to configure and call Pollinations.ai free/anonymous models and authenticated endpoints.

Features:
- Reads API key from POLLINATIONS_API_KEY environment variable or .env file
- Default free model: gpt-oss-20b (legacy anonymous endpoint)
- list_models() to query the live model catalog
- sample_text_completion() to call the free legacy model or an authenticated model
- Creates a .env.example file explaining how to set your key

Run: python scripts/pollinations_setup.py --list-models

Note: This script is intentionally lightweight and dependency-free (uses requests). Install requests if you don't have it: pip install requests
"""

from __future__ import annotations
import os
import json
import sys
from typing import Optional

try:
    import requests
except Exception:
    raise SystemExit("The 'requests' library is required. Install with: pip install requests")

# Default free legacy model available without an API key
DEFAULT_FREE_MODELS = {
    "text": "gpt-oss-20b",  # legacy OpenAI-compatible endpoint at text.pollinations.ai
}

# Endpoints
MODELS_ENDPOINT = "https://gen.pollinations.ai/v1/models"
LEGACY_CHAT_ENDPOINT = "https://text.pollinations.ai/openai/chat/completions"
AUTH_CHAT_ENDPOINT = "https://gen.pollinations.ai/v1/chat/completions"

ENV_VAR = "POLLINATIONS_API_KEY"
DOTENV_EXAMPLE = ".env.example"


def _load_dotenv_if_present(dotenv_path: str = ".env") -> None:
    """Load simple KEY=VALUE pairs from a .env file into os.environ if present.
    This is a tiny helper (not a full dotenv lib)."""
    if not os.path.isfile(dotenv_path):
        return
    with open(dotenv_path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            k, v = line.split("=", 1)
            k = k.strip()
            v = v.strip().strip('"').strip("'")
            if k and k not in os.environ:
                os.environ[k] = v


def get_api_key() -> Optional[str]:
    """Return the Pollinations API key from env or None if not set."""
    _load_dotenv_if_present()
    return os.environ.get(ENV_VAR)


def write_dotenv_example(path: str = DOTENV_EXAMPLE) -> None:
    if os.path.exists(path):
        return
    content = (
        "# Example .env for Pollinations API key\n"
        f"# Add your secret (server-side) or publishable (client) key.\n"
        f"# Export or load this variable before running scripts that call the API.\n"
        f"# Example (Linux/macOS): export {ENV_VAR}=sk_your_secret_key_here\n"
        f"# Example (.env file):\n{ENV_VAR}=sk_your_secret_key_here\n"
    )
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)


def list_models(api_key: Optional[str] = None, timeout: int = 10) -> dict:
    """Query the Pollinations model catalog.

    If api_key is provided, it will be sent as a Bearer token. If not provided,
    many model listings are still available publicly.
    Returns the parsed JSON response as a dict.
    """
    headers = {"Accept": "application/json"}
    if api_key:
        headers["Authorization"] = f"Bearer {api_key}"
    resp = requests.get(MODELS_ENDPOINT, headers=headers, timeout=timeout)
    resp.raise_for_status()
    return resp.json()


def sample_text_completion(
    prompt: str,
    model: Optional[str] = None,
    api_key: Optional[str] = None,
    timeout: int = 30,
) -> dict:
    """Run a simple chat/text completion.

    - If model is the legacy free model (gpt-oss-20b), the script calls the legacy endpoint
      that does not require an API key and uses OpenAI-compatible body.
    - Otherwise, it attempts to call the authenticated gen.pollinations.ai chat endpoint
      and will require an API key.

    Returns the parsed JSON response.
    """
    if model is None:
        model = DEFAULT_FREE_MODELS["text"]

    if model == DEFAULT_FREE_MODELS["text"]:
        # Use legacy anonymous OpenAI-compatible endpoint
        body = {
            "model": model,
            "messages": [{"role": "user", "content": prompt}],
            "max_tokens": 256,
            "temperature": 0.7,
        }
        resp = requests.post(LEGACY_CHAT_ENDPOINT, json=body, timeout=timeout)
        resp.raise_for_status()
        return resp.json()

    # Authenticated route (modern gen.pollinations.ai endpoint)
    if not api_key:
        raise ValueError("API key is required for non-legacy models. Set POLLINATIONS_API_KEY.")

    headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
    body = {
        "model": model,
        "messages": [{"role": "user", "content": prompt}],
        "max_tokens": 256,
        "temperature": 0.7,
    }
    resp = requests.post(AUTH_CHAT_ENDPOINT, headers=headers, json=body, timeout=timeout)
    resp.raise_for_status()
    return resp.json()


def _pretty_print_models_summary(models_json: dict) -> None:
    """Print a compact summary of the models response."""
    if not isinstance(models_json, dict):
        print(json.dumps(models_json, indent=2))
        return
    models = models_json.get("data") or models_json.get("models") or models_json
    if isinstance(models, list):
        print(f"Found {len(models)} models (showing id, publisher, modalities):\n")
        for m in models[:100]:
            mid = m.get("id") or m.get("name") or m.get("model")
            pub = m.get("publisher") or m.get("owner") or "-"
            modal = ",".join(sorted(m.get("modalities", []))) if m.get("modalities") else m.get("type", "-")
            print(f"- {mid}  — publisher={pub}  modalities={modal}")
    else:
        print(json.dumps(models, indent=2))


def main(argv: list[str]) -> int:
    """Small CLI for quick operations."""
    write_dotenv_example()

    api_key = get_api_key()
    if not argv:
        print("Pollinations setup helper\n")
        print("Environment variable checked:", ENV_VAR)
        print("Default free text model:", DEFAULT_FREE_MODELS["text"])
        print("Run with --list-models or --sample")
        return 0

    cmd = argv[0]
    if cmd == "--list-models":
        print("Listing models (this may show free and paid models).\n")
        try:
            models = list_models(api_key)
            _pretty_print_models_summary(models)
        except Exception as e:
            print("Failed to list models:", str(e))
            return 2
        return 0

    if cmd == "--sample":
        prompt = "\n".join(argv[1:]) if len(argv) > 1 else "Hello from Pollinations! Describe a small red fox." 
        try:
            resp = sample_text_completion(prompt, api_key=api_key)
            print(json.dumps(resp, indent=2))
        except Exception as e:
            print("Sample request failed:", str(e))
            return 3
        return 0

    print("Unknown command. Use --list-models or --sample [prompt]")
    return 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
