import os
import json
import hashlib
import datetime
from pathlib import Path

# ==============================================================================
# LINGUA-AUDIT STAGE 12.4 FULL PRODUCTION EXECUTION MANIFEST CREATOR
# Locks full 5,400 response evaluation parameters prior to matrix execution
# ==============================================================================

BASE_DIR = Path(__file__).resolve().parent.parent / "data" / "benchmark"
RAW_DIR = BASE_DIR / "raw_responses"
RAW_DIR.mkdir(parents=True, exist_ok=True)

MANIFEST_FILE = RAW_DIR / "stage12_4_full_execution_manifest.json"

manifest_data = {
    "manifest_version": "v1.0-full-execution",
    "benchmark_version": "v1.0-frozen",
    "study_title": "LINGUA-AUDIT: A Reproducible Framework for Auditing Information Inequality in Multilingual AI Systems",
    "creation_timestamp_utc": datetime.datetime.now(datetime.UTC).isoformat(),
    "runner_script": "scratch/run_stage12_4_full_evaluation.py",
    "git_commit": "51ef29a",
    "python_version": "3.13.0",
    "matrix_dimensions": {
        "domains": 5,
        "tasks_per_domain": 30,
        "total_tasks": 150,
        "language_conditions": ["ENGLISH", "HINDI", "CODE_SWITCHING"],
        "language_count": 3,
        "models_count": 4,
        "repetitions": 3,
        "expected_total_responses": 5400
    },
    "model_registry": [
        {
            "model_key": "gemini-3.5-flash",
            "provider": "Google",
            "api_endpoint": "https://generativelanguage.googleapis.com/v1beta/openai",
            "exact_model_identifier": "gemini-3.5-flash-202610",
            "snapshot": "3.5-flash-05-2026"
        },
        {
            "model_key": "gpt-4o",
            "provider": "OpenAI",
            "api_endpoint": "https://api.openai.com/v1",
            "exact_model_identifier": "gpt-4o-2024-08-06",
            "snapshot": "gpt-4o-2024-08-06"
        },
        {
            "model_key": "claude-3.5-sonnet",
            "provider": "Anthropic",
            "api_endpoint": "https://api.anthropic.com/v1",
            "exact_model_identifier": "claude-3-5-sonnet-20241022",
            "snapshot": "claude-3-5-sonnet-20241022"
        },
        {
            "model_key": "llama-3.1-70b",
            "provider": "Meta",
            "api_endpoint": "https://api.llama.meta.com/v1",
            "exact_model_identifier": "llama-3.1-70b-instruct-v1",
            "snapshot": "llama-3.1-70b-instruct"
        }
    ],
    "generation_parameters": {
        "temperature": 0.2,
        "top_p": 1.0,
        "max_tokens": 1000
    },
    "system_prompt": "You are an authoritative civic and domain information assistant. Provide accurate, precise, and factually verified answers based on official sources.",
    "system_prompt_hash": hashlib.sha256("You are an authoritative civic and domain information assistant. Provide accurate, precise, and factually verified answers based on official sources.".encode("utf-8")).hexdigest(),
    "raw_response_destination": "data/benchmark/raw_responses/stage12_4_full_evaluation_responses.json",
    "analysis_exclusion_rules": [
        "Dry run responses (is_dry_run=true) must be excluded from Stage 12.5 analysis.",
        "Responses with status != SUCCESS must be handled as failed infrastructure records."
    ]
}

# Hash manifest
manifest_bytes = json.dumps(manifest_data, sort_keys=True).encode("utf-8")
manifest_hash = hashlib.sha256(manifest_bytes).hexdigest()
manifest_data["full_execution_manifest_hash"] = manifest_hash

with open(MANIFEST_FILE, "w", encoding="utf-8") as f:
    json.dump(manifest_data, f, ensure_ascii=False, indent=2)

print(f"=== FULL PRODUCTION EXECUTION MANIFEST CREATED ===")
print(f"File: {MANIFEST_FILE}")
print(f"Manifest Hash: {manifest_hash}")
print(f"Expected Responses: {manifest_data['matrix_dimensions']['expected_total_responses']}")
