import pytest
import httpx
from app.config import settings, frozen_config
from app.core.llm_gateway import OpenAIProvider, GeminiProvider, get_llm_provider

# --- OpenAI Provider Tests ---

def test_provider_must_be_openai(monkeypatch):
    monkeypatch.setattr(settings, "USE_MOCK_LLM", False)
    monkeypatch.setattr(settings, "LLM_ENABLED", True)
    monkeypatch.setattr(settings, "LLM_PROVIDER", "groq")
    monkeypatch.setattr(settings, "OPENAI_BASE_URL", "https://api.openai.com/v1")
    monkeypatch.setattr(settings, "OPENAI_MODEL", "gpt-4o-2024-08-06")
    monkeypatch.setattr(settings, "OPENAI_API_KEY", "sk-valid-key-12345")

    provider = OpenAIProvider()
    with pytest.raises(ValueError) as exc_info:
        provider.validate_provider_configuration()
    assert "LLM_PROVIDER='openai'" in str(exc_info.value)
    assert "Third-party providers are prohibited" in str(exc_info.value)

def test_model_must_be_gpt4o_2024_08_06(monkeypatch):
    monkeypatch.setattr(settings, "USE_MOCK_LLM", False)
    monkeypatch.setattr(settings, "LLM_ENABLED", True)
    monkeypatch.setattr(settings, "LLM_PROVIDER", "openai")
    monkeypatch.setattr(settings, "OPENAI_BASE_URL", "https://api.openai.com/v1")
    monkeypatch.setattr(settings, "OPENAI_MODEL", "openai/gpt-oss-120b")
    monkeypatch.setattr(settings, "OPENAI_API_KEY", "sk-valid-key-12345")

    provider = OpenAIProvider()
    with pytest.raises(ValueError) as exc_info:
        provider.validate_provider_configuration()
    assert "Invalid model identifier" in str(exc_info.value)

def test_base_url_must_be_official_openai_endpoint(monkeypatch):
    monkeypatch.setattr(settings, "USE_MOCK_LLM", False)
    monkeypatch.setattr(settings, "LLM_ENABLED", True)
    monkeypatch.setattr(settings, "LLM_PROVIDER", "openai")
    monkeypatch.setattr(settings, "OPENAI_MODEL", "gpt-4o-2024-08-06")
    monkeypatch.setattr(settings, "OPENAI_API_KEY", "sk-valid-key-12345")

    unauthorized_urls = [
        "https://api.groq.com/openai/v1",
        "https://openrouter.ai/api/v1",
        "https://api.together.xyz/v1",
        "http://localhost:8000/v1"
    ]

    for bad_url in unauthorized_urls:
        monkeypatch.setattr(settings, "OPENAI_BASE_URL", bad_url)
        provider = OpenAIProvider()
        with pytest.raises(ValueError) as exc_info:
            provider.validate_provider_configuration()
        assert "Unauthorized LLM Base URL domain" in str(exc_info.value) or "Insecure scheme" in str(exc_info.value)

# --- Gemini Provider Tests ---

def test_gemini_provider_selection_and_validation(monkeypatch):
    monkeypatch.setattr(settings, "USE_MOCK_LLM", False)
    monkeypatch.setattr(settings, "LLM_ENABLED", True)
    monkeypatch.setattr(settings, "LLM_PROVIDER", "gemini")
    monkeypatch.setattr(settings, "GEMINI_BASE_URL", "https://generativelanguage.googleapis.com/v1beta/openai")
    monkeypatch.setattr(settings, "GEMINI_MODEL", "gemini-3.5-flash")
    monkeypatch.setattr(settings, "GEMINI_API_KEY", "AIzaSyTestGeminiKey12345")
    monkeypatch.setitem(frozen_config["production_llm_config"], "model_identifier", "gemini-3.5-flash")

    provider = get_llm_provider()
    assert isinstance(provider, GeminiProvider)
    # Should pass validation cleanly
    provider.validate_provider_configuration()

def test_gemini_base_url_domain_whitelist(monkeypatch):
    monkeypatch.setattr(settings, "USE_MOCK_LLM", False)
    monkeypatch.setattr(settings, "LLM_ENABLED", True)
    monkeypatch.setattr(settings, "LLM_PROVIDER", "gemini")
    monkeypatch.setattr(settings, "GEMINI_MODEL", "gemini-3.5-flash")
    monkeypatch.setattr(settings, "GEMINI_API_KEY", "AIzaSyTestGeminiKey12345")
    monkeypatch.setitem(frozen_config["production_llm_config"], "model_identifier", "gemini-3.5-flash")

    unauthorized_urls = [
        "https://api.groq.com/openai/v1",
        "https://api.openai.com/v1",
        "https://openrouter.ai/api/v1",
        "http://localhost:8000/v1"
    ]

    for bad_url in unauthorized_urls:
        monkeypatch.setattr(settings, "GEMINI_BASE_URL", bad_url)
        provider = GeminiProvider()
        with pytest.raises(ValueError) as exc_info:
            provider.validate_provider_configuration()
        assert "Unauthorized LLM Base URL domain" in str(exc_info.value) or "Insecure scheme" in str(exc_info.value)

def test_gemini_model_identity_lock(monkeypatch):
    monkeypatch.setattr(settings, "USE_MOCK_LLM", False)
    monkeypatch.setattr(settings, "LLM_ENABLED", True)
    monkeypatch.setattr(settings, "LLM_PROVIDER", "gemini")
    monkeypatch.setattr(settings, "GEMINI_BASE_URL", "https://generativelanguage.googleapis.com/v1beta/openai")
    monkeypatch.setattr(settings, "GEMINI_MODEL", "gemini-1.5-flash-unapproved")
    monkeypatch.setattr(settings, "GEMINI_API_KEY", "AIzaSyTestGeminiKey12345")
    monkeypatch.setitem(frozen_config["production_llm_config"], "model_identifier", "gemini-3.5-flash")

    provider = GeminiProvider()
    with pytest.raises(ValueError) as exc_info:
        provider.validate_provider_configuration()
    assert "Invalid model identifier" in str(exc_info.value)
    assert "gemini-3.5-flash" in str(exc_info.value)

def test_gemini_missing_api_key(monkeypatch):
    monkeypatch.setattr(settings, "USE_MOCK_LLM", False)
    monkeypatch.setattr(settings, "LLM_ENABLED", True)
    monkeypatch.setattr(settings, "LLM_PROVIDER", "gemini")
    monkeypatch.setattr(settings, "GEMINI_BASE_URL", "https://generativelanguage.googleapis.com/v1beta/openai")
    monkeypatch.setattr(settings, "GEMINI_MODEL", "gemini-3.5-flash")
    monkeypatch.setattr(settings, "GEMINI_API_KEY", "")
    monkeypatch.setitem(frozen_config["production_llm_config"], "model_snapshot", "gemini-3.5-flash")

    provider = GeminiProvider()
    with pytest.raises(ValueError) as exc_info:
        provider.validate_provider_configuration()
    assert "GEMINI_API_KEY is not configured" in str(exc_info.value)

def test_gemini_transport_destination_isolation(monkeypatch):
    """
    Gemini Credential Destination Test:
    Verify using mocked HTTP transport that Authorization header and request payload
    are sent ONLY to https://generativelanguage.googleapis.com/v1beta/openai/chat/completions with model gemini-3.5-flash.
    """
    monkeypatch.setattr(settings, "USE_MOCK_LLM", False)
    monkeypatch.setattr(settings, "LLM_ENABLED", True)
    monkeypatch.setattr(settings, "LLM_PROVIDER", "gemini")
    monkeypatch.setattr(settings, "GEMINI_BASE_URL", "https://generativelanguage.googleapis.com/v1beta/openai")
    monkeypatch.setattr(settings, "GEMINI_MODEL", "gemini-3.5-flash")
    monkeypatch.setattr(settings, "GEMINI_API_KEY", "AIzaSyTestValidGeminiKey999")
    monkeypatch.setitem(frozen_config["production_llm_config"], "model_snapshot", "gemini-3.5-flash")

    captured_requests = []

    def mock_handle_request(request: httpx.Request) -> httpx.Response:
        captured_requests.append(request)
        mock_body = {
            "id": "chatcmpl-gemini12345",
            "object": "chat.completion",
            "created": 1700000000,
            "model": "gemini-3.5-flash",
            "choices": [
                {
                    "index": 0,
                    "message": {
                        "role": "assistant",
                        "content": "Under PMEGP, maximum project cost for manufacturing is Rs. 50 Lakhs."
                    },
                    "finish_reason": "stop"
                }
            ],
            "usage": {
                "prompt_tokens": 42,
                "completion_tokens": 18,
                "total_tokens": 60
            }
        }
        return httpx.Response(200, json=mock_body)

    mock_transport = httpx.MockTransport(mock_handle_request)
    original_client_init = httpx.Client.__init__

    def mock_client_init(self, *args, **kwargs):
        kwargs["transport"] = mock_transport
        original_client_init(self, *args, **kwargs)

    monkeypatch.setattr(httpx.Client, "__init__", mock_client_init)

    provider = GeminiProvider()
    response = provider.generate_response(
        task_id="PMEGP",
        assigned_arm="ENGLISH_ONLY",
        persona_summary="Synthetic applicant persona",
        user_prompt="What is the maximum loan under PMEGP?",
        conversation_history=[]
    )

    assert len(captured_requests) == 1
    req = captured_requests[0]

    # Verify exact destination URL
    assert str(req.url) == "https://generativelanguage.googleapis.com/v1beta/openai/chat/completions"

    # Verify Authorization header contains ONLY the configured Gemini key
    assert req.headers["Authorization"] == "Bearer AIzaSyTestValidGeminiKey999"

    # Verify model in payload is strictly gemini-3.5-flash
    import json
    payload = json.loads(req.content.decode("utf-8"))
    assert payload["model"] == "gemini-3.5-flash"

    # Verify response structure
    assert response["model_snapshot"] == "gemini-3.5-flash"
    assert response["is_mock"] == False
    assert response["system_prompt_version"] == "v1.1.0-gemini-frozen"
    assert response["retry_count"] == 0
