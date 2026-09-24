import sys
import json
from pathlib import Path

# Add backend directory to sys.path
backend_dir = Path(__file__).resolve().parent.parent / "backend"
sys.path.insert(0, str(backend_dir))

from app.config import settings
from app.core.llm_gateway import OpenAIProvider

def main():
    # Enforce production settings for this single real test
    settings.USE_MOCK_LLM = False
    settings.LLM_ENABLED = True
    settings.LLM_PROVIDER = "openai"
    settings.OPENAI_BASE_URL = "https://api.openai.com/v1"
    settings.OPENAI_MODEL = "gpt-4o-2024-08-06"

    # Make sure API key is clean
    if not settings.OPENAI_API_KEY or not settings.OPENAI_API_KEY.strip():
        print("ERROR: OPENAI_API_KEY is missing.")
        sys.exit(1)

    settings.OPENAI_API_KEY = settings.OPENAI_API_KEY.strip()

    provider = OpenAIProvider()
    print("Initiating EXACTLY ONE real API request to OpenAI Direct API...")

    try:
        res = provider.generate_response(
            task_id="PMEGP",
            assigned_arm="ENGLISH_ONLY",
            persona_summary="Synthetic applicant persona: Rural micro-manufacturing entrepreneur seeking PMEGP entitlement details.",
            user_prompt="What is the maximum project cost and subsidy percentage for special category rural applicants under PMEGP?",
            conversation_history=[]
        )

        prompt_tokens = res["tokens_used"]["prompt_tokens"]
        completion_tokens = res["tokens_used"]["completion_tokens"]
        total_tokens = res["tokens_used"]["total_tokens"]

        # Cost calculation based on OpenAI gpt-4o pricing ($2.50 / 1M input, $10.00 / 1M output)
        prompt_cost = (prompt_tokens / 1_000_000.0) * 2.50
        completion_cost = (completion_tokens / 1_000_000.0) * 10.00
        total_cost = prompt_cost + completion_cost

        summary = {
            "Provider": "OpenAI Direct API",
            "Endpoint": "https://api.openai.com/v1/chat/completions",
            "RequestedModel": settings.OPENAI_MODEL,
            "ActualModel": res["model_snapshot"],
            "HTTPStatus": 200,
            "LatencyMs": res["latency_ms"],
            "PromptTokens": prompt_tokens,
            "CompletionTokens": completion_tokens,
            "TotalTokens": total_tokens,
            "RetryCount": res["retry_count"],
            "LanguageLeakageFlag": res["language_leakage_flag"],
            "IsMock": res["is_mock"],
            "EstimatedCostUSD": f"${total_cost:.6f}",
            "ResponseSnippet": res["text"][:150] + "..."
        }

        output_path = Path(__file__).resolve().parent / "real_smoke_test_result.json"
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(summary, f, indent=2)

        print("\n--- SMOKE TEST SUCCESS ---")
        print(json.dumps(summary, indent=2))

    except Exception as e:
        print(f"\n--- SMOKE TEST FAILED ---")
        print(f"Error: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()
