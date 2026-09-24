import pytest
from app.randomization.engine import RandomizationEngine
from app.db.models import Participant, ConsentLog, ScreeningLog, LanguageBackground, AILiteracy, RandomizationAllocation

def test_randomization_cutoff_strata(db):
    engine = RandomizationEngine(db)
    assert engine.get_stratum(20) == "LOW"
    assert engine.get_stratum(35) == "LOW"
    assert engine.get_stratum(36) == "HIGH"
    assert engine.get_stratum(50) == "HIGH"

def test_randomization_requires_all_prerequisites(db):
    engine = RandomizationEngine(db)
    p = Participant()
    db.add(p)
    db.commit()

    is_eligible, msg = engine.verify_eligibility_for_randomization(p.participant_id)
    assert not is_eligible
    assert "Consent" in msg

def test_randomization_allocation_balance(db):
    # Simulate 36 participants in LOW stratum and 36 in HIGH stratum
    engine = RandomizationEngine(db)

    low_counts = {"ENGLISH_ONLY": 0, "HINDI_ONLY": 0, "CODE_SWITCHING": 0}
    high_counts = {"ENGLISH_ONLY": 0, "HINDI_ONLY": 0, "CODE_SWITCHING": 0}

    for i in range(36):
        p = Participant()
        db.add(p)
        db.commit()
        db.add(ConsentLog(participant_id=p.participant_id, agreed_to_terms=True, confirmed_age_residency=True))
        db.add(ScreeningLog(participant_id=p.participant_id, score_english=3, score_hindi=3, passed=True, raw_responses={}))
        db.add(LanguageBackground(
            participant_id=p.participant_id, aoa_english=6, aoa_hindi=0, primary_home_lang="Hindi",
            medium_instruction_school="Hindi", medium_instruction_higher="English",
            self_read_en=8, self_write_en=8, self_speak_en=8, self_read_hi=9, self_write_hi=9, self_speak_hi=9,
            freq_daily_en=50, freq_daily_hi=40, freq_daily_cs=10, ai_use_en=70, ai_use_hi=20, ai_use_mixed=10
        ))
        db.add(AILiteracy(participant_id=p.participant_id, raw_responses={}, total_score=25, stratum="LOW"))
        db.commit()

        alloc = engine.allocate_participant(p.participant_id)
        low_counts[alloc.assigned_arm] += 1

    for i in range(36):
        p = Participant()
        db.add(p)
        db.commit()
        db.add(ConsentLog(participant_id=p.participant_id, agreed_to_terms=True, confirmed_age_residency=True))
        db.add(ScreeningLog(participant_id=p.participant_id, score_english=3, score_hindi=3, passed=True, raw_responses={}))
        db.add(LanguageBackground(
            participant_id=p.participant_id, aoa_english=6, aoa_hindi=0, primary_home_lang="Hindi",
            medium_instruction_school="Hindi", medium_instruction_higher="English",
            self_read_en=8, self_write_en=8, self_speak_en=8, self_read_hi=9, self_write_hi=9, self_speak_hi=9,
            freq_daily_en=50, freq_daily_hi=40, freq_daily_cs=10, ai_use_en=70, ai_use_hi=20, ai_use_mixed=10
        ))
        db.add(AILiteracy(participant_id=p.participant_id, raw_responses={}, total_score=48, stratum="HIGH"))
        db.commit()

        alloc = engine.allocate_participant(p.participant_id)
        high_counts[alloc.assigned_arm] += 1

    # In permuted block randomization, max imbalance between arms at any point is bounded by max block size
    low_vals = list(low_counts.values())
    assert max(low_vals) - min(low_vals) <= 2

    high_vals = list(high_counts.values())
    assert max(high_vals) - min(high_vals) <= 2

    # Verify that completed blocks in DB contain exactly equal numbers of each arm
    allocs = db.query(RandomizationAllocation).filter(RandomizationAllocation.stratum == "LOW").all()
    block_map = {}
    block_size_map = {}
    for a in allocs:
        block_map.setdefault(a.block_id, []).append(a.assigned_arm)
        block_size_map[a.block_id] = a.block_size

    for block_id, arms in block_map.items():
        expected_size = block_size_map[block_id]
        if len(arms) == expected_size:
            if expected_size == 3:
                assert set(arms) == {"ENGLISH_ONLY", "HINDI_ONLY", "CODE_SWITCHING"}
            elif expected_size == 6:
                assert arms.count("ENGLISH_ONLY") == 2
                assert arms.count("HINDI_ONLY") == 2
                assert arms.count("CODE_SWITCHING") == 2
