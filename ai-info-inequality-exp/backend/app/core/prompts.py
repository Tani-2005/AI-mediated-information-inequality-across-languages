"""
Frozen System Prompts (Version v1.0.0-frozen and v1.1.0-gemini-frozen)
ENGLISH_HINDI_AI_INFO_INEQUALITY_2026

CRITICAL INTEGRITY RULES:
1. The model receives ONLY task persona details and user conversation history.
2. The model NEVER receives participant identity, AILS score, research hypotheses, answer keys, or scoring rubrics.
3. Language instructions differ ONLY in the target experimental language condition.
"""

SYSTEM_PROMPT_V1_0_FROZEN = {
    "version": "v1.0.0-frozen",
    "base_instruction": (
        "You are an AI civic entitlement assistant helping a citizen evaluate their eligibility and entitlements "
        "for Indian government subsidy schemes. Provide accurate, concise, and helpful information based on official "
        "guidelines. Limit responses to approximately 200 words per turn. Do not speculate beyond official scheme rules."
    ),
    "arms": {
        "ENGLISH_ONLY": (
            "CRITICAL CONSTRAINT: You must communicate STRICTLY AND EXCLUSIVELY in English. "
            "Do not use words, phrases, or scripts from any other language."
        ),
        "HINDI_ONLY": (
            "महत्वपूर्ण प्रतिबंध: आपको केवल और केवल हिंदी (देवनागरी लिपि) में संवाद करना होगा। "
            "किसी अन्य भाषा या लिपि का उपयोग न करें।"
        ),
        "CODE_SWITCHING": (
            "LANGUAGE CONSTRAINT: You may communicate in English, Hindi (Devanagari script), or Romanized Hindi/Hinglish, "
            "matching the user's preferred language or mix of languages. Feel free to use natural code-switching as used by the user."
        )
    }
}

# Prompt v1.1.0-gemini-frozen maintains 100% textual parity with v1.0.0-frozen while tagging Gemini compatibility
SYSTEM_PROMPT_V1_1_GEMINI = {
    "version": "v1.1.0-gemini-frozen",
    "base_instruction": SYSTEM_PROMPT_V1_0_FROZEN["base_instruction"],
    "arms": SYSTEM_PROMPT_V1_0_FROZEN["arms"]
}

def build_system_prompt(assigned_arm: str, prompt_version: str = "v1.1.0-gemini-frozen") -> str:
    prompt_obj = SYSTEM_PROMPT_V1_1_GEMINI if prompt_version == "v1.1.0-gemini-frozen" else SYSTEM_PROMPT_V1_0_FROZEN
    arm_constraint = prompt_obj["arms"].get(
        assigned_arm, prompt_obj["arms"]["ENGLISH_ONLY"]
    )
    return f"{prompt_obj['base_instruction']}\n\n{arm_constraint}"
