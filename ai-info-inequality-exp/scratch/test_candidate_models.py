import sys
import json
from pathlib import Path
import httpx

backend_dir = Path(__file__).resolve().parent.parent / "backend"
sys.path.insert(0, str(backend_dir))

from app.config import settings

def test_model(model_name: str):
    key = settings.GEMINI_API_KEY.strip()
    url = f"https://generativelanguage.googleapis.com/v1beta/openai/chat/completions"
    headers = {
        "Authorization": f"Bearer {key}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": model_name,
        "messages": [
            {"role": "system", "content": "You are a helpful assistant. Reply concisely."},
            {"role": "user", "content": "What is PMEGP?"}
        ],
        "temperature": 0.2,
        "max_tokens": 100
    }

    try:
        resp = httpx.post(url, headers=headers, json=payload, timeout=15.0)
        print(f"Model: {model_name:<25} | Status: {resp.status_code}")
        if resp.status_code == 200:
            data = resp.json()
            reply = data["choices"][0]["message"]["content"]
            model_ret = data.get("model", model_name)
            usage = data.get("usage", {})
            print(f"   -> Success! Actual Model Returned: {model_ret}")
            print(f"   -> Usage: {usage}")
            print(f"   -> Response snippet: {reply[:80]}...")
            return True, resp.status_code, data
        else:
            print(f"   -> Failed: {resp.text[:120]}")
            return False, resp.status_code, resp.text
    except Exception as e:
        print(f"   -> Exception: {str(e)}")
        return False, 500, str(e)

def main():
    candidates = [
        "gemini-2.5-flash",
        "gemini-3.8-flash",
        "gemini-3.5-flash",
        "gemini-1.5-flash",
        "gemini-2.0-flash"
    ]
    print("Testing candidate production models against official Google OpenAI-compatible endpoint...\n")
    results = {}
    for cand in candidates:
        ok, code, res = test_model(cand)
        results[cand] = {"ok": ok, "status": code, "res": res}

if __name__ == "__main__":
    main()
