import pytest
from app.config import settings
from app.core.prompts import build_system_prompt, SYSTEM_PROMPT_V1_0_FROZEN, SYSTEM_PROMPT_V1_1_GEMINI
from app.core.llm_gateway import (
    get_llm_provider,
    MockLLMProvider,
    OpenAIProvider,
    GeminiProvider,
    detect_language_leakage
)

def test_provider_factory_switching(monkeypatch):
    # Mock mode -> MockLLMProvider
    monkeypatch.setattr(settings, "USE_MOCK_LLM", True)
    assert isinstance(get_llm_provider(), MockLLMProvider)

    # Production OpenAI -> OpenAIProvider
    monkeypatch.setattr(settings, "USE_MOCK_LLM", False)
    monkeypatch.setattr(settings, "LLM_PROVIDER", "openai")
    assert isinstance(get_llm_provider(), OpenAIProvider)

    # Production Gemini -> GeminiProvider
    monkeypatch.setattr(settings, "LLM_PROVIDER", "gemini")
    assert isinstance(get_llm_provider(), GeminiProvider)

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
    monkeypatch.setattr(settings, "LLM_PROVIDER", "gemini")
    monkeypatch.setattr(settings, "GEMINI_BASE_URL", "https://generativelanguage.googleapis.com/v1beta/openai")
    monkeypatch.setattr(settings, "GEMINI_MODEL", "gemini-3.5-flash")
    monkeypatch.setattr(settings, "GEMINI_API_KEY", "")

    provider = get_llm_provider()
    with pytest.raises(ValueError) as exc_info:
        provider.generate_response(
            task_id="PMEGP",
            assigned_arm="ENGLISH_ONLY",
            persona_summary="Test persona",
            user_prompt="Hello",
            conversation_history=[]
        )
    assert "GEMINI_API_KEY is not configured" in str(exc_info.value)

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
