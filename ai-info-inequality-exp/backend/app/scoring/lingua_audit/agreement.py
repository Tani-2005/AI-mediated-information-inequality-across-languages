"""
Legitimate Inter-Rater Reliability & Agreement Statistics Engine.
Implements quadratic weighted Cohen's kappa for ordinal metrics (M5, M6, M7)
and diagnostic-guarded ICC(2,1) for continuous/interval measures (M2a).
"""

from typing import List, Tuple, Dict, Any, Optional
import numpy as np


def compute_quadratic_weighted_kappa(
    rater1: List[int],
    rater2: List[int],
    min_rating: int = 0,
    max_rating: int = 4
) -> Tuple[Optional[float], Dict[str, Any]]:
    """
    Computes quadratic weighted Cohen's kappa for ordinal ratings.
    Weights: w_ij = 1 - (i - j)^2 / (max_rating - min_rating)^2.
    """
    if len(rater1) != len(rater2):
        raise ValueError("Rater lists must have equal length")

    n = len(rater1)
    if n == 0:
        return None, {"error": "Empty ratings list"}

    k = max_rating - min_rating + 1
    conf_mat = np.zeros((k, k), dtype=float)

    for r1, r2 in zip(rater1, rater2):
        if not (min_rating <= r1 <= max_rating and min_rating <= r2 <= max_rating):
            raise ValueError(f"Rating out of bounds [{min_rating}, {max_rating}]: r1={r1}, r2={r2}")
        conf_mat[r1 - min_rating, r2 - min_rating] += 1.0

    # Build quadratic weight matrix
    weights = np.zeros((k, k), dtype=float)
    denom_weight = float((k - 1) ** 2) if k > 1 else 1.0
    for i in range(k):
        for j in range(k):
            weights[i, j] = 1.0 - ((i - j) ** 2) / denom_weight

    # Marginal totals
    r1_marginals = np.sum(conf_mat, axis=1)
    r2_marginals = np.sum(conf_mat, axis=0)

    # Expected agreement matrix under independence
    expected_mat = np.outer(r1_marginals, r2_marginals) / float(n)

    po_weighted = np.sum(weights * conf_mat) / float(n)
    pe_weighted = np.sum(weights * expected_mat) / float(n)

    if pe_weighted >= 1.0 - 1e-12:
        # Zero variance / complete marginal degeneracy
        return None, {
            "status": "UNDEFINED_ZERO_VARIANCE",
            "po": po_weighted,
            "pe": pe_weighted,
            "n": n,
            "contingency_matrix": conf_mat.tolist()
        }

    kappa = (po_weighted - pe_weighted) / (1.0 - pe_weighted)

    diagnostics = {
        "status": "VALID",
        "n": n,
        "po_weighted": float(po_weighted),
        "pe_weighted": float(pe_weighted),
        "raw_agreement_rate": float(np.trace(conf_mat) / n),
        "contingency_matrix": conf_mat.tolist()
    }

    return float(kappa), diagnostics


def compute_icc_2_1_with_diagnostics(
    matrix: np.ndarray
) -> Tuple[Optional[float], Dict[str, Any]]:
    """
    Computes ICC(2,1) (Two-way random effects, single rater, absolute agreement).
    Includes rigorous diagnostic checks for zero-variance, identity degeneration,
    and missingness.

    Formula:
    ICC(2,1) = (MS_R - MS_E) / (MS_R + (k - 1)*MS_E + (k / n)*(MS_C - MS_E))
    """
    if matrix.ndim != 2 or matrix.shape[1] != 2:
        raise ValueError("Matrix must be of shape (n_targets, 2)")

    n, k = matrix.shape
    if n < 2:
        return None, {"status": "INSUFFICIENT_OBSERVATIONS", "n": n}

    # Check for NaN / missing
    if np.isnan(matrix).any():
        return None, {"status": "CONTAINS_NAN"}

    # Total variance
    total_var = np.var(matrix)
    if total_var < 1e-12:
        return None, {
            "status": "DEGENERATE_ZERO_TOTAL_VARIANCE",
            "message": "All ratings across all subjects are identical. ICC is undefined."
        }

    # Check if rater 1 and rater 2 are bitwise identical
    is_identical_columns = np.allclose(matrix[:, 0], matrix[:, 1])

    # Subject means, column means, grand mean
    row_means = np.mean(matrix, axis=1)
    col_means = np.mean(matrix, axis=0)
    grand_mean = np.mean(matrix)

    ss_total = np.sum((matrix - grand_mean) ** 2)
    ss_rows = k * np.sum((row_means - grand_mean) ** 2)
    ss_cols = n * np.sum((col_means - grand_mean) ** 2)
    ss_error = ss_total - ss_rows - ss_cols

    # Ensure non-negative error due to floating precision
    ss_error = max(0.0, ss_error)

    df_rows = n - 1
    df_cols = k - 1
    df_error = (n - 1) * (k - 1)

    ms_rows = ss_rows / df_rows
    ms_cols = ss_cols / df_cols
    ms_error = ss_error / df_error if df_error > 0 else 0.0

    denom = ms_rows + (k - 1) * ms_error + (k / n) * (ms_cols - ms_error)

    if denom <= 1e-12:
        return None, {
            "status": "ZERO_DENOMINATOR",
            "ms_rows": ms_rows,
            "ms_error": ms_error
        }

    icc = (ms_rows - ms_error) / denom

    diagnostics = {
        "status": "VALID",
        "n": n,
        "k": k,
        "ms_rows": float(ms_rows),
        "ms_cols": float(ms_cols),
        "ms_error": float(ms_error),
        "is_identical_columns": bool(is_identical_columns),
        "warning": "Identical vectors detected (likely cloned record)" if is_identical_columns else None
    }

    return float(icc), diagnostics
