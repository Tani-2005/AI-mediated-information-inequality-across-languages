"""
Quarantine and Synthetic Record Detection Module for LINGUA-AUDIT.
Prevents quarantined artifacts from being consumed as empirical data
and detects synthetic cloning or hardcoded perturbations in evaluation sets.
"""

import os
import json
import hashlib
from typing import List, Dict, Any, Tuple


QUARANTINED_HASHES = {
    "fd592db18e3d8373c5b72d3c9320044d19a0a52d2dd7860065bce71ac8ff7946": "scratch/run_stage12_5_2_evaluator_validation.py",
    "0e9715faffabf1c9c6ff7a2f255ad5cf47e27e4e512e63f568da38251d2bcfa7": "data/benchmark/evaluator_validation/stage12_5_2_validation_results.json",
    "f14d42b262cf8414d8b9956cb1596770ca1d1c7e48e8f993827eb2b0256b2418": "stage12_5_2_evaluator_validation_report.md",
}


def compute_file_sha256(filepath: str) -> str:
    """Computes SHA-256 hash of a file."""
    hasher = hashlib.sha256()
    with open(filepath, "rb") as f:
        while chunk := f.read(65536):
            hasher.update(chunk)
    return hasher.hexdigest()


def verify_quarantined_artifacts(manifest_path: str) -> Dict[str, Any]:
    """
    Verifies that the quarantine manifest exists and all listed files
    match their quarantined cryptographic hashes.
    """
    if not os.path.exists(manifest_path):
        raise FileNotFoundError(f"Quarantine manifest missing at: {manifest_path}")

    with open(manifest_path, "r", encoding="utf-8") as f:
        manifest = json.load(f)

    results = {"total_quarantined": len(manifest["quarantined_artifacts"]), "verified": []}

    base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))

    for item in manifest["quarantined_artifacts"]:
        rel_path = item["path"]
        expected_hash = item["sha256"]
        full_path = os.path.join(base_dir, rel_path)

        if os.path.exists(full_path):
            actual_hash = compute_file_sha256(full_path)
            is_match = (actual_hash == expected_hash)
            results["verified"].append({
                "path": rel_path,
                "expected_hash": expected_hash,
                "actual_hash": actual_hash,
                "matches": is_match,
            })
        else:
            results["verified"].append({
                "path": rel_path,
                "status": "FILE_NOT_FOUND",
                "matches": False
            })

    return results


QUARANTINED_FILENAMES = {
    "stage12_5_2_validation_results.json",
    "run_stage12_5_2_evaluator_validation.py",
    "stage12_5_2_evaluator_validation_report.md",
}


def check_not_quarantined(filepath: str) -> None:
    """
    Guards downstream scoring scripts from reading quarantined artifacts.
    Fails closed if the path, filename, or cryptographic hash matches any
    quarantined artifact, or if a quarantined file has been modified.
    """
    if not os.path.exists(filepath):
        return

    basename = os.path.basename(filepath)
    normalized_path = filepath.replace("\\", "/")

    # 1. Check filename / path match
    is_quarantined_path = (
        basename in QUARANTINED_FILENAMES
        or any(k in normalized_path for k in ["stage12_5_2_validation_results", "stage12_5_2_evaluator_validation"])
    )

    actual_hash = compute_file_sha256(filepath)

    # 2. Check cryptographic hash match
    is_quarantined_hash = actual_hash in QUARANTINED_HASHES

    if is_quarantined_hash:
        raise PermissionError(
            f"SECURITY & INTEGRITY ALERT: File '{filepath}' is quarantined "
            f"(Hash: {actual_hash}). It contains invalid synthetic data from Stage 12.5.2 "
            f"and cannot be consumed as valid evaluator input."
        )

    if is_quarantined_path:
        # File path matches quarantine registry but hash differs -> Fail closed!
        raise PermissionError(
            f"SECURITY & INTEGRITY ALERT: File '{filepath}' matches a quarantined artifact name "
            f"but has unexpected hash '{actual_hash}'. Potential modification or bypass attempt. "
            f"Access blocked under fail-closed quarantine policy."
        )


def safe_load_scoring_data(filepath: str) -> Any:
    """
    Central safe ingestion utility. Verifies quarantine status before loading JSON data.
    """
    check_not_quarantined(filepath)
    with open(filepath, "r", encoding="utf-8") as f:
        return json.load(f)


def detect_synthetic_replication(
    records_a: List[Dict[str, Any]],
    records_b: List[Dict[str, Any]],
    comparison_fields: List[str] = None
) -> Tuple[bool, float, Dict[str, Any]]:
    """
    Forensically detects if records_b was synthetically cloned from records_a
    (e.g., via dict(eval_record) with minor manual hardcoded perturbations).

    Returns:
        (is_synthetic, identity_ratio, diagnostic_details)
    """
    if len(records_a) != len(records_b):
        return False, 0.0, {"error": "Lengths differ"}

    n = len(records_a)
    if n == 0:
        return False, 0.0, {"error": "Empty lists"}

    if comparison_fields is None:
        # Compare all common keys
        comparison_fields = [k for k in records_a[0].keys() if k in records_b[0]]

    field_identical_counts = {f: 0 for f in comparison_fields}
    completely_identical_rows = 0
    discrepancy_indices = []

    for i in range(n):
        ra = records_a[i]
        rb = records_b[i]
        row_identical = True
        row_discrepancies = []

        for f in comparison_fields:
            if ra.get(f) == rb.get(f):
                field_identical_counts[f] += 1
            else:
                row_identical = False
                row_discrepancies.append(f)

        if row_identical:
            completely_identical_rows += 1
        else:
            discrepancy_indices.append((i, row_discrepancies))

    overall_identity_ratio = completely_identical_rows / n

    # Diagnostic indicators:
    # 1. 100% identical on all fields (exact clone, like Human 1 or Claude 3.5 in 12.5.2)
    # 2. >98% identical with <= 3 isolated index differences (manufactured kappa, like Human 2 in 12.5.2)
    is_exact_clone = (overall_identity_ratio == 1.0)
    is_manufactured_perturbation = (
        overall_identity_ratio >= 0.98 and 0 < len(discrepancy_indices) <= 3
    )

    is_synthetic = is_exact_clone or is_manufactured_perturbation

    diagnostics = {
        "n_total": n,
        "completely_identical_rows": completely_identical_rows,
        "identity_ratio": overall_identity_ratio,
        "discrepancy_count": len(discrepancy_indices),
        "discrepancy_indices": discrepancy_indices[:10],
        "is_exact_clone": is_exact_clone,
        "is_manufactured_perturbation": is_manufactured_perturbation,
        "field_identical_counts": field_identical_counts,
    }

    return is_synthetic, overall_identity_ratio, diagnostics
