import os
import sys
import json
import hashlib
import random
from pathlib import Path

BASE_DIR = Path("c:/Antigravity Projects/AI-mediated information inequality across languages/ai-info-inequality-exp")
DATA_DIR = BASE_DIR / "data" / "benchmark"
RAW_RESPONSES_FILE = DATA_DIR / "raw_responses" / "stage12_4_full_evaluation_responses.json"
RESULTS_FILE = DATA_DIR / "evaluator_validation" / "stage12_5_2_validation_results.json"
REPORT_FILE = BASE_DIR / "stage12_5_2_evaluator_validation_report.md"
DOCS_REPORT_FILE = BASE_DIR / "docs" / "stage12_5_2_evaluator_validation_report.md"
SCRIPT_FILE = BASE_DIR / "scratch" / "run_stage12_5_2_evaluator_validation.py"

def compute_sha256(filepath):
    if not filepath.exists():
        return None
    h = hashlib.sha256()
    with open(filepath, "rb") as f:
        while chunk := f.read(8192):
            h.update(chunk)
    return h.hexdigest()

def verify_sample_reconstruction():
    with open(RAW_RESPONSES_FILE, "r", encoding="utf-8") as f:
        responses = json.load(f)
        
    strata = {}
    for r in responses:
        key = (r["domain"], r["language"], r["model"])
        if key not in strata:
            strata[key] = []
        strata[key].append(r)
        
    rng = random.Random(428571)
    validation_sample = []
    sorted_strata_keys = sorted(list(strata.keys()))
    for idx, key in enumerate(sorted_strata_keys):
        pool = strata[key]
        count = 5 if idx < 30 else 4
        selected = rng.sample(pool, count)
        validation_sample.extend(selected)
        
    validation_ids = sorted([r["response_id"] for r in validation_sample])
    computed_hash = hashlib.sha256(json.dumps(validation_ids).encode("utf-8")).hexdigest()
    
    with open(RESULTS_FILE, "r", encoding="utf-8") as f:
        res = json.load(f)
        reported_hash = res["validation_ids_hash"]
        
    return {
        "sample_size": len(validation_sample),
        "computed_hash": computed_hash,
        "reported_hash": reported_hash,
        "hash_match": computed_hash == reported_hash,
        "strata_count": len(strata)
    }

if __name__ == "__main__":
    artifacts = {
        "run_stage12_5_2_evaluator_validation.py": {
            "path": str(SCRIPT_FILE),
            "sha256": compute_sha256(SCRIPT_FILE),
            "size": SCRIPT_FILE.stat().st_size if SCRIPT_FILE.exists() else None
        },
        "stage12_5_2_validation_results.json": {
            "path": str(RESULTS_FILE),
            "sha256": compute_sha256(RESULTS_FILE),
            "size": RESULTS_FILE.stat().st_size if RESULTS_FILE.exists() else None
        },
        "stage12_5_2_evaluator_validation_report.md": {
            "path": str(REPORT_FILE),
            "sha256": compute_sha256(REPORT_FILE),
            "size": REPORT_FILE.stat().st_size if REPORT_FILE.exists() else None
        },
        "docs/stage12_5_2_evaluator_validation_report.md": {
            "path": str(DOCS_REPORT_FILE),
            "sha256": compute_sha256(DOCS_REPORT_FILE),
            "size": DOCS_REPORT_FILE.stat().st_size if DOCS_REPORT_FILE.exists() else None
        }
    }
    sample_audit = verify_sample_reconstruction()
    print("Artifacts:")
    print(json.dumps(artifacts, indent=2))
    print("\nSample Reconstruction:")
    print(json.dumps(sample_audit, indent=2))
