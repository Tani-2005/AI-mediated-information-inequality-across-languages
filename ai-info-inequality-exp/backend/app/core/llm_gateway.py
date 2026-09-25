import re
import time
import datetime
from abc import ABC, abstractmethod
from typing import Dict, Any, List, Optional
import httpx
from app.config import settings, frozen_config
from app.core.prompts import build_system_prompt, SYSTEM_PROMPT_V1_0_FROZEN

DEVANAGARI_REGEX = re.compile(r'[\u0900-\u097F]')

def detect_language_leakage(assigned_arm: str, text: str) -> bool:
    if not text or not text.strip():
        return False
    if assigned_arm == "ENGLISH_ONLY":
        # Leakage if Devanagari script is present
        return bool(DEVANAGARI_REGEX.search(text))
    elif assigned_arm == "HINDI_ONLY":
        # Leakage if Devanagari script is completely missing from a non-empty Hindi response
        return not bool(DEVANAGARI_REGEX.search(text))
    return False

class LLMResponse(ABC):
    pass

class LLMProvider(ABC):
    @abstractmethod
    def generate_response(
        self,
        task_id: str,
        assigned_arm: str,
        persona_summary: str,
        user_prompt: str,
        conversation_history: List[Dict[str, str]]
    ) -> Dict[str, Any]:
        pass

class MockLLMProvider(LLMProvider):
    MOCK_RESPONSES = {
        "ENGLISH_ONLY": {
            "PMEGP": "Under PMEGP for manufacturing units, the maximum project cost allowed is Rs. 50 Lakhs. For a Special Category rural applicant, the subsidy rate is 35%. Mandatory documents include Aadhaar Card, EDP Certificate, DPR, and Rural/Caste Certificate.",
            "PM_VISHWAKARMA": "Under PM Vishwakarma, traditional artisans qualify for a First Tranche concessional loan of up to Rs. 1,00,000 at 5% interest rate. During basic skill training, a daily stipend of Rs. 500 is provided, along with a modern toolkit incentive voucher grant of Rs. 15,000.",
            "PM_SVANIDHI": "Under PM SVANidhi, street vendors can receive a First Tranche working capital loan of up to Rs. 10,000 for a 1-year tenure. An annual interest subsidy of 7% is credited quarterly, and vendors can earn up to Rs. 1,200 annually in digital transaction cashback incentives."
        },
        "HINDI_ONLY": {
            "PMEGP": "PMEGP योजना के तहत विनिर्माण (Manufacturing) इकाइयों के लिए अधिकतम परियोजना लागत रु 50 लाख है। ग्रामीण क्षेत्र के विशेष वर्ग के आवेदकों के लिए सब्सिडी दर 35% है। आवश्यक दस्तावेजों में आधार कार्ड, ईडीपी प्रमाणपत्र, डीपीआर और ग्रामीण/जाति प्रमाणपत्र शामिल हैं।",
            "PM_VISHWAKARMA": "पीएम विश्वकर्मा योजना के तहत पारंपरिक कारीगर 5% ब्याज दर पर रु 1,00,000 तक के प्रथम चरण रियायती ऋण के पात्र हैं। बुनियादी कौशल प्रशिक्षण के दौरान रु 500 प्रति दिन का वजीफा और रु 15,000 का आधुनिक टूलकिट वाउचर अनुदान दिया जाता है।",
            "PM_SVANidhi": "पीएम स्वनिधि योजना के तहत रेहड़ी-पटरी विक्रेता 1 वर्ष की अवधि के लिए रु 10,000 तक का प्रथम चरण कार्यशील पूंजी ऋण प्राप्त कर सकते हैं। 7% का वार्षिक ब्याज अनुदान त्रैमासिक जमा किया जाता है, और डिजिटल लेनदेन पर रु 1,200 तक वार्षिक कैशबैल प्रोत्साहन मिलता है।"
        },
        "CODE_SWITCHING": {
            "PMEGP": "PMEGP scheme ke under manufacturing units ke liye maximum project cost Rs. 50 Lakhs allowed hai. Special category rural applicants ko 35% subsidy (margin money) milti hai. Key documents: Aadhaar, EDP Training Certificate, DPR, and Rural Certificate.",
            "PM_VISHWAKARMA": "PM Vishwakarma scheme mein traditional artisans ko First Tranche mein 5% interest rate par Rs. 1,00,000 tak concessional loan milta hai. Basic skill training ke dauran Rs. 500/day stipend aur Rs. 15,000 ka toolkit voucher grant milta hai.",
            "PM_SVANidhi": "PM SVANidhi scheme ke tehat street vendors ko 1st tranche mein Rs. 10,000 tak working capital loan 1 year tenure ke liye milta hai. 7% annual interest subsidy milti hai aur Rs. 1,200 max annual digital cashback incentive milta hai."
        }
    }

    def generate_response(
        self,
        task_id: str,
        assigned_arm: str,
        persona_summary: str,
        user_prompt: str,
        conversation_history: List[Dict[str, str]]
    ) -> Dict[str, Any]:
        start_time = time.time()
        arm_dict = self.MOCK_RESPONSES.get(assigned_arm, self.MOCK_RESPONSES["ENGLISH_ONLY"])
        reply_text = arm_dict.get(task_id, "Mock AI assistant response for task.")
        latency_ms = int((time.time() - start_time) * 1000)

        leakage_flag = detect_language_leakage(assigned_arm, reply_text)

        return {
            "text": reply_text,
            "model_snapshot": "development-mock-stub",
            "system_prompt_version": SYSTEM_PROMPT_V1_0_FROZEN["version"],
            "timestamp": datetime.datetime.now(datetime.UTC).isoformat(),
            "latency_ms": max(latency_ms, 120),
            "tokens_used": {"prompt_tokens": 45, "completion_tokens": 55, "total_tokens": 100},
            "retry_count": 0,
            "error_status": None,
            "language_leakage_flag": leakage_flag,
            "is_mock": True
        }

class OpenAIProvider(LLMProvider):
    ALLOWED_HOSTS = {"api.openai.com"}

    def validate_provider_configuration(self):
        """
        Enforce strict provider architecture.
        Production protocol requires OpenAI Direct API with gpt-4o-2024-08-06.
        Zero fallback to Groq, third-party gateways, or alternate models.
        """
        # 1. Provider Check
        provider = (settings.LLM_PROVIDER or "").strip().lower()
        if provider != "openai":
            raise ValueError(
                f"Invalid LLM_PROVIDER '{settings.LLM_PROVIDER}'. "
                "Frozen protocol strictly requires LLM_PROVIDER='openai'. Third-party providers are prohibited."
            )

        # 2. Base URL / Endpoint Destination Check
        base_url = (settings.OPENAI_BASE_URL or "").strip()
        from urllib.parse import urlparse
        parsed_url = urlparse(base_url)
        if not parsed_url.scheme or not parsed_url.netloc:
            raise ValueError(f"Invalid OPENAI_BASE_URL format: '{base_url}'. Must be a valid absolute HTTPS URL.")

        if parsed_url.scheme.lower() != "https":
            raise ValueError(f"Insecure scheme in OPENAI_BASE_URL: '{base_url}'. Must use HTTPS.")

        hostname = parsed_url.netloc.split(":")[0].lower()
        if hostname not in self.ALLOWED_HOSTS:
            raise ValueError(
                f"Unauthorized LLM Base URL domain '{hostname}'. "
                "Frozen protocol strictly requires official OpenAI direct API domain ('api.openai.com'). "
                "Third-party gateways (Groq, OpenRouter, Together, etc.) are strictly prohibited."
            )

        # 3. Model Identifier Check
        model = (settings.OPENAI_MODEL or "").strip()
        expected_model = frozen_config["production_llm_config"]["model_snapshot"]
        if model != expected_model or model != "gpt-4o-2024-08-06":
            raise ValueError(
                f"Invalid model snapshot '{model}'. "
                f"Frozen protocol strictly requires '{expected_model}'. Alternate models or aliases are prohibited."
            )

        # 4. Credential Format Safety Check
        key = (settings.OPENAI_API_KEY or "").strip()
        if not key:
            raise ValueError("OPENAI_API_KEY is not configured.")
        if key.startswith("gsk_"):
            raise ValueError(
                "Credential routing error: OPENAI_API_KEY contains a Groq API key ('gsk_...'). "
                "Groq credentials cannot be used with OpenAI Direct API."
            )

    def generate_response(
        self,
        task_id: str,
        assigned_arm: str,
        persona_summary: str,
        user_prompt: str,
        conversation_history: List[Dict[str, str]]
    ) -> Dict[str, Any]:
        if not settings.LLM_ENABLED:
            raise RuntimeError("Emergency Kill Switch: LLM_ENABLED is set to False.")

        # Strict Integrity Audit & Validation before making any network request
        self.validate_provider_configuration()

        system_prompt = build_system_prompt(assigned_arm)
        model_name = settings.OPENAI_MODEL

        temperature = frozen_config["production_llm_config"]["temperature"]
        top_p = frozen_config["production_llm_config"]["top_p"]
        max_tokens = frozen_config["production_llm_config"]["max_tokens"]
        timeout_sec = frozen_config["production_llm_config"]["timeout_ms"] / 1000.0

        messages_payload = [{"role": "system", "content": f"{system_prompt}\n\nPersona Context:\n{persona_summary}"}]
        for turn in conversation_history:
            messages_payload.append({"role": turn["role"], "content": turn["content"]})
        messages_payload.append({"role": "user", "content": user_prompt})

        headers = {
            "Authorization": f"Bearer {settings.OPENAI_API_KEY.strip()}",
            "Content-Type": "application/json"
        }

        request_body = {
            "model": model_name,
            "messages": messages_payload,
            "temperature": temperature,
            "top_p": top_p,
            "max_tokens": max_tokens
        }

        endpoint_url = f"{settings.OPENAI_BASE_URL.rstrip('/')}/chat/completions"

        start_time = time.time()
        retries = 0
        last_error = None

        # Max 1 retry permitted for HTTP 5xx or connection timeout only
        for attempt in range(2):
            try:
                with httpx.Client(timeout=timeout_sec) as client:
                    response = client.post(
                        endpoint_url,
                        headers=headers,
                        json=request_body
                    )
                
                latency_ms = int((time.time() - start_time) * 1000)

                if response.status_code == 200:
                    data = response.json()
                    choice = data["choices"][0]
                    reply_text = choice["message"]["content"]
                    usage = data.get("usage", {})
                    actual_model = data.get("model", model_name)

                    leakage_flag = detect_language_leakage(assigned_arm, reply_text)

                    return {
                        "text": reply_text,
                        "model_snapshot": actual_model,
                        "system_prompt_version": SYSTEM_PROMPT_V1_0_FROZEN["version"],
                        "timestamp": datetime.datetime.now(datetime.UTC).isoformat(),
                        "latency_ms": latency_ms,
                        "tokens_used": {
                            "prompt_tokens": usage.get("prompt_tokens", 0),
                            "completion_tokens": usage.get("completion_tokens", 0),
                            "total_tokens": usage.get("total_tokens", 0)
                        },
                        "retry_count": retries,
                        "error_status": None,
                        "language_leakage_flag": leakage_flag,
                        "is_mock": False
                    }
                
                # If 5xx server error, attempt 1 retry
                if response.status_code >= 500 and attempt == 0:
                    retries += 1
                    time.sleep(1.0)
                    continue
                else:
                    # Client errors (4xx) or unrecoverable error -> Do NOT retry
                    raise RuntimeError(f"OpenAI API error HTTP {response.status_code}: {response.text}")

            except (httpx.TimeoutException, httpx.NetworkError) as net_err:
                last_error = net_err
                if attempt == 0:
                    retries += 1
                    time.sleep(1.0)
                    continue
                else:
                    raise RuntimeError(f"OpenAI API network timeout after retry: {str(net_err)}")

        raise RuntimeError(f"OpenAI API call failed: {str(last_error)}")

def get_llm_provider() -> LLMProvider:
    if settings.USE_MOCK_LLM:
        return MockLLMProvider()

    provider_name = (settings.LLM_PROVIDER or "").strip().lower()
    if provider_name == "gemini":
        return GeminiProvider()
    elif provider_name == "openai":
        return OpenAIProvider()
    else:
        raise ValueError(
            f"Unsupported LLM_PROVIDER '{settings.LLM_PROVIDER}'. "
            "Supported production providers are 'gemini' and 'openai'."
        )

class GeminiProvider(LLMProvider):
    ALLOWED_HOSTS = {"generativelanguage.googleapis.com"}

    def validate_provider_configuration(self):
        """
        Enforce strict provider architecture for Google Gemini API.
        Production protocol requires Google Gemini API with gemini-2.5-flash.
        Zero fallback to Groq, OpenAI, third-party gateways, or alternate models.
        """
        # 1. Provider Check
        provider = (settings.LLM_PROVIDER or "").strip().lower()
        if provider != "gemini":
            raise ValueError(
                f"Invalid LLM_PROVIDER '{settings.LLM_PROVIDER}'. "
                "Active protocol strictly requires LLM_PROVIDER='gemini'. Third-party providers are prohibited."
            )

        # 2. Base URL / Endpoint Destination Check
        base_url = (settings.GEMINI_BASE_URL or "").strip()
        from urllib.parse import urlparse
        parsed_url = urlparse(base_url)
        if not parsed_url.scheme or not parsed_url.netloc:
            raise ValueError(f"Invalid GEMINI_BASE_URL format: '{base_url}'. Must be a valid absolute HTTPS URL.")

        if parsed_url.scheme.lower() != "https":
            raise ValueError(f"Insecure scheme in GEMINI_BASE_URL: '{base_url}'. Must use HTTPS.")

        hostname = parsed_url.netloc.split(":")[0].lower()
        if hostname not in self.ALLOWED_HOSTS:
            raise ValueError(
                f"Unauthorized LLM Base URL domain '{hostname}'. "
                "Protocol strictly requires official Google Gemini API domain ('generativelanguage.googleapis.com'). "
                "Third-party gateways (Groq, OpenRouter, Together, etc.) are strictly prohibited."
            )

        # 3. Model Identifier Check
        model = (settings.GEMINI_MODEL or "").strip()
        expected_model = frozen_config["production_llm_config"]["model_snapshot"]
        if model != expected_model or model != "gemini-3.5-flash":
            raise ValueError(
                f"Invalid model snapshot '{model}'. "
                f"Active protocol strictly requires '{expected_model}'. Alternate models or aliases are prohibited."
            )

        # 4. Credential Format Safety Check
        key = (settings.GEMINI_API_KEY or "").strip()
        if not key:
            raise ValueError("GEMINI_API_KEY is not configured.")

    def generate_response(
        self,
        task_id: str,
        assigned_arm: str,
        persona_summary: str,
        user_prompt: str,
        conversation_history: List[Dict[str, str]]
    ) -> Dict[str, Any]:
        if not settings.LLM_ENABLED:
            raise RuntimeError("Emergency Kill Switch: LLM_ENABLED is set to False.")

        self.validate_provider_configuration()

        system_prompt = build_system_prompt(assigned_arm, prompt_version="v1.1.0-gemini-frozen")
        model_name = settings.GEMINI_MODEL

        temperature = frozen_config["production_llm_config"]["temperature"]
        top_p = frozen_config["production_llm_config"]["top_p"]
        max_tokens = frozen_config["production_llm_config"]["max_tokens"]
        timeout_sec = frozen_config["production_llm_config"]["timeout_ms"] / 1000.0

        messages_payload = [{"role": "system", "content": f"{system_prompt}\n\nPersona Context:\n{persona_summary}"}]
        for turn in conversation_history:
            messages_payload.append({"role": turn["role"], "content": turn["content"]})
        messages_payload.append({"role": "user", "content": user_prompt})

        headers = {
            "Authorization": f"Bearer {settings.GEMINI_API_KEY.strip()}",
            "Content-Type": "application/json"
        }

        request_body = {
            "model": model_name,
            "messages": messages_payload,
            "temperature": temperature,
            "top_p": top_p,
            "max_tokens": max_tokens
        }

        endpoint_url = f"{settings.GEMINI_BASE_URL.rstrip('/')}/chat/completions"

        start_time = time.time()
        retries = 0
        last_error = None

        for attempt in range(2):
            try:
                with httpx.Client(timeout=timeout_sec) as client:
                    response = client.post(
                        endpoint_url,
                        headers=headers,
                        json=request_body
                    )
                
                latency_ms = int((time.time() - start_time) * 1000)

                if response.status_code == 200:
                    data = response.json()
                    choice = data["choices"][0]
                    reply_text = choice["message"]["content"]
                    usage = data.get("usage", {})
                    actual_model = data.get("model", model_name)

                    leakage_flag = detect_language_leakage(assigned_arm, reply_text)

                    return {
                        "text": reply_text,
                        "model_snapshot": actual_model,
                        "system_prompt_version": "v1.1.0-gemini-frozen",
                        "timestamp": datetime.datetime.now(datetime.UTC).isoformat(),
                        "latency_ms": latency_ms,
                        "tokens_used": {
                            "prompt_tokens": usage.get("prompt_tokens", 0),
                            "completion_tokens": usage.get("completion_tokens", 0),
                            "total_tokens": usage.get("total_tokens", 0)
                        },
                        "retry_count": retries,
                        "error_status": None,
                        "language_leakage_flag": leakage_flag,
                        "is_mock": False
                    }
                
                if response.status_code >= 500 and attempt == 0:
                    retries += 1
                    time.sleep(1.0)
                    continue
                else:
                    raise RuntimeError(f"Google Gemini API error HTTP {response.status_code}: {response.text}")

            except (httpx.TimeoutException, httpx.NetworkError) as net_err:
                last_error = net_err
                if attempt == 0:
                    retries += 1
                    time.sleep(1.0)
                    continue
                else:
                    raise RuntimeError(f"Google Gemini API network timeout after retry: {str(net_err)}")

        raise RuntimeError(f"Google Gemini API call failed: {str(last_error)}")
