import os
import sys
import json
import hashlib
from pathlib import Path

# Add backend to path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "backend"))

BASE_DIR = Path(__file__).resolve().parent.parent / "data" / "benchmark"
TASKS_DIR = BASE_DIR / "tasks"
RAW_RESPONSES_DIR = BASE_DIR / "raw_responses"

MASTER_REGISTRY_FILE = BASE_DIR / "master_task_registry_150.json"
BENCHMARK_MANIFEST_FILE = BASE_DIR / "benchmark_manifest.json"
EXECUTION_MANIFEST_FILE = RAW_RESPONSES_DIR / "stage12_4_full_execution_manifest.json"
RESPONSES_FILE = RAW_RESPONSES_DIR / "stage12_4_full_evaluation_responses.json"
INTEGRITY_MANIFEST_FILE = RAW_RESPONSES_DIR / "stage12_4_dataset_integrity_manifest.json"

EXPECTED_DATASET_HASH = "296bb1650f06cc7934f16e90ef662f9c9b0207971344b0935ee02704b8bf4248"
EXPECTED_MANIFEST_HASH = "46375b1657b93712dfcb490b0812f76c6491f464aaa10ed0bbcba1452a48d5a5"
EXPECTED_SYSTEM_PROMPT_HASH = "102cd78d14c3e8a2e29d1c6ca620671f89f29bacd8795548a863f6f0599e8b94"
EXPECTED_BENCHMARK_VERSION = "v1.0-frozen"

LANG_MAP = {
    "ENGLISH": "english",
    "HINDI": "hindi",
    "CODE_SWITCHING": "code_switch"
}

def compute_hash(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()

def run_dataset_integrity_audit():
    print("=== STARTING STAGE 12.4B DATASET INTEGRITY & CELL-LEVEL PROVENANCE AUDIT ===")

    # 1. Load Files
    if not RESPONSES_FILE.exists():
        raise FileNotFoundError(f"Responses file missing: {RESPONSES_FILE}")
    if not MASTER_REGISTRY_FILE.exists():
        raise FileNotFoundError(f"Master registry file missing: {MASTER_REGISTRY_FILE}")
    if not EXECUTION_MANIFEST_FILE.exists():
        raise FileNotFoundError(f"Execution manifest missing: {EXECUTION_MANIFEST_FILE}")

    with open(RESPONSES_FILE, "r", encoding="utf-8") as f:
        responses = json.load(f)

    with open(MASTER_REGISTRY_FILE, "r", encoding="utf-8") as f:
        master_registry = json.load(f)

    with open(EXECUTION_MANIFEST_FILE, "r", encoding="utf-8") as f:
        execution_manifest = json.load(f)

    # 2. Recompute Dataset Hash
    dataset_bytes = json.dumps(responses, sort_keys=True).encode("utf-8")
    actual_dataset_hash = hashlib.sha256(dataset_bytes).hexdigest()
    print(f"Dataset SHA256 Hash: {actual_dataset_hash}")
    dataset_hash_match = (actual_dataset_hash == EXPECTED_DATASET_HASH)
    print(f"Dataset Hash Match: {dataset_hash_match}")

    # 3. Execution Manifest Hash Verification
    actual_manifest_hash = execution_manifest.get("full_execution_manifest_hash")
    manifest_hash_match = (actual_manifest_hash == EXPECTED_MANIFEST_HASH)
    print(f"Manifest Hash Match: {manifest_hash_match} ({actual_manifest_hash})")

    # Build Master Task Map
    master_tasks = {t["task_id"]: t for t in master_registry}
    
    # Expected Dimensions
    domains = ["Healthcare", "Education", "Public_Services", "Finance", "General_Knowledge"]
    languages = ["ENGLISH", "HINDI", "CODE_SWITCHING"]
    models = ["gemini-3.5-flash", "gpt-4o", "claude-3.5-sonnet", "llama-3.1-70b"]
    repetitions = [1, 2, 3]

    expected_cells = set()
    for tid in master_tasks.keys():
        for lang in languages:
            for mod in models:
                for rep in repetitions:
                    expected_cells.add((tid, lang, mod, rep))

    print(f"Expected Unique Factorial Cells: {len(expected_cells)}")

    # Audit Metrics Tracking
    observed_cells = set()
    cell_occurrences = {}
    duplicate_records = []
    
    prompt_hash_matches = 0
    prompt_hash_failures = 0
    
    response_hash_matches = 0
    response_hash_failures = 0

    dry_run_records = 0
    benchmark_version_mismatches = 0
    execution_manifest_mismatches = 0
    execution_id_mismatches = 0
    parameter_mismatches = 0
    provenance_failures = 0

    request_ids = set()
    response_ids = set()
    execution_ids = set()

    model_counts = {m: 0 for m in models}
    language_counts = {l: 0 for l in languages}
    domain_counts = {d: 0 for d in domains}
    repetition_counts = {f"R{r}": 0 for r in repetitions}

    first_exec_id = responses[0]["execution_id"] if responses else None

    # Iterative Record Inspection
    for r in responses:
        tid = r.get("task_id")
        lang = r.get("language")
        mod = r.get("model")
        rep = r.get("repetition")
        
        cell_key = (tid, lang, mod, rep)
        observed_cells.add(cell_key)
        
        cell_occurrences[cell_key] = cell_occurrences.get(cell_key, 0) + 1
        if cell_occurrences[cell_key] > 1:
            duplicate_records.append(r)

        # Count dimensions
        if mod in model_counts:
            model_counts[mod] += 1
        if lang in language_counts:
            language_counts[lang] += 1
        if r.get("domain") in domain_counts:
            domain_counts[r.get("domain")] += 1
        if rep in [1, 2, 3]:
            repetition_counts[f"R{rep}"] += 1

        # Check Task ID
        if tid not in master_tasks:
            provenance_failures += 1

        # Check Task Domain, Family, Variant parity
        task_ref = master_tasks.get(tid, {})
        if r.get("domain") != task_ref.get("domain"):
            provenance_failures += 1
        
        calc_family = f"{tid.split('-')[0]}-FAM-{(int(tid.split('-')[1])-1)//6 + 1:02d}"
        calc_variant = f"VAR-{(int(tid.split('-')[1])-1)%6 + 1:02d}"
        if r.get("scenario_family_id") != calc_family or r.get("variant_id") != calc_variant:
            provenance_failures += 1

        # Prompt Hash Check
        lang_key = LANG_MAP.get(lang)
        expected_prompt = task_ref.get("prompts", {}).get(lang_key, "") if task_ref else ""
        expected_prompt_hash = compute_hash(expected_prompt) if expected_prompt else ""
        
        stored_prompt_hash = r.get("prompt_hash")
        recomputed_prompt_hash = compute_hash(r.get("prompt_text", ""))
        
        if stored_prompt_hash == expected_prompt_hash and recomputed_prompt_hash == expected_prompt_hash:
            prompt_hash_matches += 1
        else:
            prompt_hash_failures += 1

        # Response Hash Check
        stored_resp_hash = r.get("response_hash")
        recomputed_resp_hash = compute_hash(r.get("raw_response", ""))
        if stored_resp_hash == recomputed_resp_hash and stored_resp_hash != "":
            response_hash_matches += 1
        else:
            response_hash_failures += 1

        # Dry Run Check
        if r.get("is_dry_run") is not False:
            dry_run_records += 1

        # Manifest Binding
        if r.get("execution_manifest_hash") != EXPECTED_MANIFEST_HASH:
            execution_manifest_mismatches += 1

        # Benchmark Version
        if r.get("benchmark_version") != EXPECTED_BENCHMARK_VERSION:
            benchmark_version_mismatches += 1

        # Execution ID consistency
        exec_id = r.get("execution_id")
        execution_ids.add(exec_id)
        if exec_id != first_exec_id:
            execution_id_mismatches += 1

        # Parameter Consistency
        gen_params = r.get("generation_parameters", {})
        if gen_params.get("temperature") != 0.2 or gen_params.get("top_p") != 1.0 or gen_params.get("max_tokens") != 1000:
            parameter_mismatches += 1
        if r.get("system_prompt_hash") != EXPECTED_SYSTEM_PROMPT_HASH:
            parameter_mismatches += 1

        # IDs
        request_ids.add(r.get("request_id"))
        response_ids.add(r.get("response_id"))

    missing_cells = list(expected_cells - observed_cells)
    duplicate_cell_keys = [k for k, v in cell_occurrences.items() if v > 1]

    print("\n--- FACTORIAL CELL AUDIT RESULTS ---")
    print(f"Total Records: {len(responses)}")
    print(f"Unique Observed Cells: {len(observed_cells)} / {len(expected_cells)}")
    print(f"Missing Cells: {len(missing_cells)}")
    print(f"Duplicate Cells: {len(duplicate_cell_keys)}")
    print(f"Prompt Hash Matches: {prompt_hash_matches} / {len(responses)}")
    print(f"Prompt Hash Failures: {prompt_hash_failures}")
    print(f"Response Hash Matches: {response_hash_matches} / {len(responses)}")
    print(f"Response Hash Failures: {response_hash_failures}")
    print(f"Dry Run Contamination Records: {dry_run_records}")
    print(f"Execution Manifest Mismatches: {execution_manifest_mismatches}")
    print(f"Benchmark Version Mismatches: {benchmark_version_mismatches}")
    print(f"Parameter Mismatches: {parameter_mismatches}")
    print(f"Request ID Uniqueness: {len(request_ids)} / {len(responses)}")
    print(f"Response ID Uniqueness: {len(response_ids)} / {len(responses)}")
    print(f"Execution IDs Present: {len(execution_ids)} ({list(execution_ids)})")

    with open(BENCHMARK_MANIFEST_FILE, "r", encoding="utf-8") as f:
        bm_manifest = json.load(f)

    # Compute master task registry hash
    registry_bytes = json.dumps(master_registry, sort_keys=True).encode("utf-8")
    benchmark_hash = hashlib.sha256(registry_bytes).hexdigest()

    # Generate Dataset Integrity Manifest JSON
    integrity_manifest = {
        "execution_id": first_exec_id,
        "benchmark_version": EXPECTED_BENCHMARK_VERSION,
        "benchmark_hash": benchmark_hash,
        "execution_manifest_hash": EXPECTED_MANIFEST_HASH,
        "dataset_hash": actual_dataset_hash,
        "total_records": len(responses),
        "unique_factorial_cells": len(observed_cells),
        "expected_factorial_cells": len(expected_cells),
        "duplicate_cells": len(duplicate_cell_keys),
        "missing_cells": len(missing_cells),
        "prompt_hash_matches": prompt_hash_matches,
        "prompt_hash_failures": prompt_hash_failures,
        "response_hash_matches": response_hash_matches,
        "response_hash_failures": response_hash_failures,
        "domain_counts": domain_counts,
        "language_counts": language_counts,
        "model_counts": model_counts,
        "repetition_counts": repetition_counts,
        "dry_run_records": dry_run_records,
        "benchmark_version_mismatches": benchmark_version_mismatches,
        "execution_manifest_mismatches": execution_manifest_mismatches,
        "execution_id_mismatches": execution_id_mismatches,
        "parameter_mismatches": parameter_mismatches,
        "provenance_failures": provenance_failures,
        "request_id_uniqueness": len(request_ids) == len(responses),
        "response_id_uniqueness": len(response_ids) == len(responses),
        "final_gate_verdict": "DATASET VERIFIED AND CLEARED FOR STAGE 12.5" if (
            dataset_hash_match and
            manifest_hash_match and
            len(observed_cells) == 5400 and
            len(missing_cells) == 0 and
            len(duplicate_cell_keys) == 0 and
            prompt_hash_failures == 0 and
            response_hash_failures == 0 and
            dry_run_records == 0 and
            benchmark_version_mismatches == 0 and
            execution_manifest_mismatches == 0 and
            parameter_mismatches == 0 and
            provenance_failures == 0
        ) else "DATASET INTEGRITY FAILURE — DO NOT ANALYZE"
    }

    with open(INTEGRITY_MANIFEST_FILE, "w", encoding="utf-8") as f:
        json.dump(integrity_manifest, f, ensure_ascii=False, indent=2)

    print(f"\nIntegrity Manifest Saved: {INTEGRITY_MANIFEST_FILE}")
    print(f"Final Gate Verdict: {integrity_manifest['final_gate_verdict']}")
    return integrity_manifest

if __name__ == "__main__":
    run_dataset_integrity_audit()
