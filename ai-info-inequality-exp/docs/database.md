# Database & Schema Documentation

The database implements 12 relational entities using SQLAlchemy & Alembic:
1. `participants`: Master pseudonymous session tracking (`participant_id` UUID v4, `status`, `is_pilot`, `ip_hash`).
2. `consent_logs`: Consent timestamps & checkboxes.
3. `screening_logs`: Bilingual passage MCQ scores (English & Hindi) and pass/fail flag.
4. `language_background`: LEAP-Q variables (AoA, home language, schooling, 1-10 proficiencies, usage %).
5. `ai_literacy`: 12-item AILS responses, total score, and computed stratum (`LOW`/`HIGH`).
6. `randomization_allocations`: Server-side allocation record (`stratum`, `block_id`, `block_size`, `assigned_arm`).
7. `task_sessions`: Scenario tracking (`task_id`, `position`, `order_id`, `status`).
8. `messages`: User prompts & AI responses (`message_text`, `latency_ms`, `tokens_used`, `language_leakage_flag`).
9. `telemetry_events`: High-resolution interaction logs (`event_type`, `event_data` JSON).
10. `final_decisions`: Submitted answers, confidence rating (1-7), calculated score (0-10), score breakdown.
11. `post_task_measures`: Raw NASA-TLX workload 6-item scores and feedback comments.
12. `technical_errors`: API timeouts, retries, and network errors.
