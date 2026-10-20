import re

with open('paper/LINGUA_AUDIT_manuscript_draft.md', 'r', encoding='utf-8') as f:
    lines = f.readlines()

print(f"Total lines: {len(lines)}")

patterns = [
    (r"\*\*#", "Double asterisk before hash"),
    (r"\\#", "Escaped hash"),
    (r"\\\*", "Escaped asterisk"),
    (r"\\_", "Escaped underscore"),
    (r"\\`", "Escaped backtick"),
    (r"\*\*\s*##", "Bolded heading"),
    (r"\*\*\s*\*\*", "Empty bold or nested bold"),
    (r"hundreds of millions", "Population claim: hundreds of millions"),
    (r"predominantly", "Population claim: predominantly"),
    (r"statutory benchmark", "Terminology: statutory benchmark"),
    (r"necessary methodological", "Terminology: necessary methodological"),
    (r"\bfirst\b", "Novelty: first"),
    (r"\bunique\b", "Novelty: unique"),
    (r"\bunprecedented\b", "Novelty: unprecedented"),
]

for idx, line in enumerate(lines, 1):
    for pat, desc in patterns:
        m = re.findall(pat, line, re.IGNORECASE)
        if m:
            print(f"Line {idx} [{desc}]: {line.strip()[:100]}")
