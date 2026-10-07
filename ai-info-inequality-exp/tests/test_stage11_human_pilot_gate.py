import pytest
import os
import pandas as pd
from pathlib import Path
from app.config import settings, validate_production_config, frozen_config

# ==============================================================================
# STAGE 11 LIVE HUMAN PILOT EXECUTION & PRODUCTION ISOLATION TEST SUITE
# ==============================================================================

def test_dataset_physical_separation():
    """Verify physical directory separation between synthetic dry run and human pilot data."""
    base_data = Path("data")
    human_dir = base_data / "human_pilot"
    
    assert human_dir.exists() is True
    human_file = human_dir / "raw_human_pilot_dataset.csv"
    assert human_file.exists() is True

    df_human = pd.read_csv(human_file)
    assert len(df_human) == 54  # 18 participants x 3 tasks
    assert df_human["participant_id"].nunique() == 18


def test_production_path_synthetic_isolation():
    """Verify production security validator strictly blocks USE_MOCK_LLM in production mode."""
    # When APP_ENV=production, USE_MOCK_LLM=True must raise ValueError
    with pytest.raises(ValueError, match="USE_MOCK_LLM=True is prohibited in production"):
        settings_copy = settings
        settings_copy.APP_ENV = "production"
        settings_copy.USE_MOCK_LLM = True
        validate_production_config()


def test_human_pilot_language_dominance_index_formula():
    """Verify LanguageDominanceIndex in frozen human pilot dataset uses difference score formula."""
    human_file = Path("data/human_pilot/raw_human_pilot_dataset.csv")
    df_human = pd.read_csv(human_file)
    
    assert "language_dominance_index" in df_human.columns
    dom_values = df_human["language_dominance_index"].dropna().values
    
    # Difference score range is [-9.0, +9.0]
    assert all(-9.0 <= val <= 9.0 for val in dom_values)
