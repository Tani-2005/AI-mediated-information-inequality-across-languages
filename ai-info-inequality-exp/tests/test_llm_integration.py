import pytest
from app.config import settings
from app.core.prompts import build_system_prompt, SYSTEM_PROMPT_V1_0_FROZEN
from app.core.llm_gateway import (
    get_llm_provider,
    MockLLMProvider,
    OpenAIProvider,
    detect_language_leakage
)

def test_provider_switching_mock_vs_openai(monkeypatch):
    monkeypatch.setattr(settings, "USE_MOCK_LLM", True)
    provider_mock = get_llm_provider()
    assert isinstance(provider_mock, MockLLMProvider)

    monkeypatch.setattr(settings, "USE_MOCK_LLM", False)
    provider_openai = get_llm_provider()
    assert isinstance(provider_openai, OpenAIProvider)

def test_emergency_kill_switch(monkeypatch):
    monkeypatch.setattr(settings, "USE_MOCK_LLM", False)
    monkeypatch.setattr(settings, "LLM_ENABLED", False)

    provider = get_llm_provider()
    with pytest.raises(RuntimeError) as exc_info:
        provider.generate_response(
            task_id="PMEGP",
            assigned_arm="ENGLISH_ONLY",
            persona_summary="Test persona",
            user_prompt="Hello",
            conversation_history=[]
        )
    assert "Emergency Kill Switch" in str(exc_info.value)

def test_missing_api_key_handling(monkeypatch):
    monkeypatch.setattr(settings, "USE_MOCK_LLM", False)
    monkeypatch.setattr(settings, "LLM_ENABLED", True)
    monkeypatch.setattr(settings, "LLM_PROVIDER", "openai")
    monkeypatch.setattr(settings, "OPENAI_BASE_URL", "https://api.openai.com/v1")
    monkeypatch.setattr(settings, "OPENAI_MODEL", "gpt-4o-2024-08-06")
    monkeypatch.setattr(settings, "OPENAI_API_KEY", "")

    provider = get_llm_provider()
    with pytest.raises(ValueError) as exc_info:
        provider.generate_response(
            task_id="PMEGP",
            assigned_arm="ENGLISH_ONLY",
            persona_summary="Test persona",
            user_prompt="Hello",
            conversation_history=[]
        )
    assert "OPENAI_API_KEY is not configured" in str(exc_info.value)

def test_language_leakage_detector():
    # English arm with Devanagari script -> Leakage = True
    assert detect_language_leakage("ENGLISH_ONLY", "Hello, यह एक परीक्षा है") == True
    # English arm with English text -> Leakage = False
    assert detect_language_leakage("ENGLISH_ONLY", "Hello, this is a test") == False

    # Hindi arm with Devanagari text -> Leakage = False
    assert detect_language_leakage("HINDI_ONLY", "यह एक परीक्षा है") == False
    # Hindi arm with purely English text -> Leakage = True
    assert detect_language_leakage("HINDI_ONLY", "This is purely English text") == True

    # Code-switching arm -> Leakage = False always
    assert detect_language_leakage("CODE_SWITCHING", "PMEGP scheme ke under 50 Lakhs max cost hai") == False

def test_prompt_isolation_security():
    prompt = build_system_prompt("ENGLISH_ONLY")
    # Verify no answer keys or participant metadata exist in system prompt
    assert "ground_truth" not in prompt.lower()
    assert "ails" not in prompt.lower()
    assert "score" not in prompt.lower()
    assert "participant_id" not in prompt.lower()
    assert "50 Lakhs" not in prompt
    assert "100000" not in prompt

def test_mock_provider_response_generation():
    provider = MockLLMProvider()
    res = provider.generate_response(
        task_id="PMEGP",
        assigned_arm="ENGLISH_ONLY",
        persona_summary="Persona summary",
        user_prompt="What is the maximum loan under PMEGP?",
        conversation_history=[]
    )
    assert res["is_mock"] == True
    assert "50 Lakhs" in res["text"]
    assert res["model_snapshot"] == "development-mock-stub"
    assert res["system_prompt_version"] == SYSTEM_PROMPT_V1_0_FROZEN["version"]
    assert res["language_leakage_flag"] == False
