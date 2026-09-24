import pytest
import httpx
from app.config import settings
from app.core.llm_gateway import OpenAIProvider, get_llm_provider

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
    assert "Invalid model snapshot" in str(exc_info.value)
    assert "gpt-4o-2024-08-06" in str(exc_info.value)

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
        "http://localhost:8000/v1",
        "https://custom-gateway.internal/v1"
    ]

    for bad_url in unauthorized_urls:
        monkeypatch.setattr(settings, "OPENAI_BASE_URL", bad_url)
        provider = OpenAIProvider()
        with pytest.raises(ValueError) as exc_info:
            provider.validate_provider_configuration()
        assert "Unauthorized LLM Base URL domain" in str(exc_info.value) or "Insecure scheme" in str(exc_info.value)

def test_prohibit_groq_key_prefix(monkeypatch):
    monkeypatch.setattr(settings, "USE_MOCK_LLM", False)
    monkeypatch.setattr(settings, "LLM_ENABLED", True)
    monkeypatch.setattr(settings, "LLM_PROVIDER", "openai")
    monkeypatch.setattr(settings, "OPENAI_BASE_URL", "https://api.openai.com/v1")
    monkeypatch.setattr(settings, "OPENAI_MODEL", "gpt-4o-2024-08-06")
    monkeypatch.setattr(settings, "OPENAI_API_KEY", "gsk_test_groq_key_12345")

    provider = OpenAIProvider()
    with pytest.raises(ValueError) as exc_info:
        provider.validate_provider_configuration()
    assert "Groq API key ('gsk_...')" in str(exc_info.value)

def test_credential_destination_transport_isolation(monkeypatch):
    """
    Credential Destination Test:
    Verify using mocked HTTP transport that Authorization header and request payload
    are sent ONLY to https://api.openai.com/v1/chat/completions with model gpt-4o-2024-08-06.
    """
    monkeypatch.setattr(settings, "USE_MOCK_LLM", False)
    monkeypatch.setattr(settings, "LLM_ENABLED", True)
    monkeypatch.setattr(settings, "LLM_PROVIDER", "openai")
    monkeypatch.setattr(settings, "OPENAI_BASE_URL", "https://api.openai.com/v1")
    monkeypatch.setattr(settings, "OPENAI_MODEL", "gpt-4o-2024-08-06")
    monkeypatch.setattr(settings, "OPENAI_API_KEY", "sk-mock-valid-openai-key-99999")

    captured_requests = []

    def mock_handle_request(request: httpx.Request) -> httpx.Response:
        captured_requests.append(request)
        mock_body = {
            "id": "chatcmpl-test12345",
            "object": "chat.completion",
            "created": 1700000000,
            "model": "gpt-4o-2024-08-06",
            "choices": [
                {
                    "index": 0,
                    "message": {
                        "role": "assistant",
                        "content": "Under PMEGP, max manufacturing project cost is Rs. 50 Lakhs."
                    },
                    "finish_reason": "stop"
                }
            ],
            "usage": {
                "prompt_tokens": 50,
                "completion_tokens": 20,
                "total_tokens": 70
            }
        }
        return httpx.Response(200, json=mock_body)

    mock_transport = httpx.MockTransport(mock_handle_request)
    original_client_init = httpx.Client.__init__

    def mock_client_init(self, *args, **kwargs):
        kwargs["transport"] = mock_transport
        original_client_init(self, *args, **kwargs)

    monkeypatch.setattr(httpx.Client, "__init__", mock_client_init)

    provider = OpenAIProvider()
    response = provider.generate_response(
        task_id="PMEGP",
        assigned_arm="ENGLISH_ONLY",
        persona_summary="Synthetic test persona",
        user_prompt="What is the maximum project cost under PMEGP?",
        conversation_history=[]
    )

    assert len(captured_requests) == 1
    req = captured_requests[0]

    # Verify exact destination URL
    assert str(req.url) == "https://api.openai.com/v1/chat/completions"

    # Verify Authorization header contains ONLY the configured key and is sent to api.openai.com
    assert req.headers["Authorization"] == "Bearer sk-mock-valid-openai-key-99999"

    # Verify model in payload is strictly gpt-4o-2024-08-06
    import json
    payload = json.loads(req.content.decode("utf-8"))
    assert payload["model"] == "gpt-4o-2024-08-06"

    # Verify response structure
    assert response["model_snapshot"] == "gpt-4o-2024-08-06"
    assert response["is_mock"] == False
    assert response["retry_count"] == 0
