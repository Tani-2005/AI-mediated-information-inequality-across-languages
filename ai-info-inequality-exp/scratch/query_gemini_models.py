import sys
import json
from pathlib import Path
import httpx

backend_dir = Path(__file__).resolve().parent.parent / "backend"
sys.path.insert(0, str(backend_dir))

from app.config import settings

def main():
    key = settings.GEMINI_API_KEY.strip()
    if not key:
        print("ERROR: GEMINI_API_KEY is not configured.")
        sys.exit(1)

    url = f"https://generativelanguage.googleapis.com/v1beta/models?key={key}"
    print(f"Querying official Google Gemini models API at https://generativelanguage.googleapis.com/v1beta/models...")

    try:
        resp = httpx.get(url, timeout=15.0)
        print(f"HTTP Status: {resp.status_code}")
        if resp.status_code == 200:
            data = resp.json()
            models = data.get("models", [])
            print(f"Total models returned by Google API: {len(models)}\n")
            
            output_path = Path(__file__).resolve().parent / "available_gemini_models.json"
            with open(output_path, "w", encoding="utf-8") as f:
                json.dump(models, f, indent=2)

            for m in models:
                name = m.get("name", "").replace("models/", "")
                disp = m.get("displayName", "")
                methods = m.get("supportedGenerationMethods", [])
                print(f"ID: {name:<30} | Name: {disp:<30} | Methods: {methods}")
        else:
            print(f"Error listing models HTTP {resp.status_code}: {resp.text}")
    except Exception as e:
        print(f"Network error querying models API: {str(e)}")

if __name__ == "__main__":
    main()
