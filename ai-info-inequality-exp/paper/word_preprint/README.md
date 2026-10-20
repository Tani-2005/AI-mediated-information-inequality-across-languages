# LINGUA-AUDIT Word Preprint Deliverable

This directory contains the publication-quality, editable Microsoft Word preprint of the **LINGUA-AUDIT** manuscript:

- **Word Document:** [`LINGUA_AUDIT_preprint.docx`](./LINGUA_AUDIT_preprint.docx)
- **High-Resolution Figure 1:** [`figure1_framework_overview.png`](./figure1_framework_overview.png)
- **Verification PDF:** [`LINGUA_AUDIT_preprint.pdf`](./LINGUA_AUDIT_preprint.pdf)
- **Rendered Verification Pages:** [`rendered_pages/`](./rendered_pages/) (Pages 1–14 rendered at 150 DPI for visual layout inspection)

---

## 1. Manuscript Metadata

- **Title:** LINGUA-AUDIT: Auditing Information Inequality in Multilingual AI Systems
- **Author:** Tanya Deep
- **Affiliation:** BMS Institute of Technology and Management, Bengaluru, India
- **Email:** `1by23is231@bmsit.in`
- **Authorship Notice:** Sole-authored manuscript. No co-authors, supervisors, or acknowledgements have been added.

---

## 2. Document Typography and Layout Standards

The document was formatted to single-column, venue-neutral academic preprint standards:

| Layout Attribute | Specification | Implementation Detail |
| :--- | :--- | :--- |
| **Page Size** | A4 (210 mm × 297 mm) | Standard international preprint size |
| **Margins** | 1.0 inch (25.4 mm) on all four sides | Uniform printable width: 6.27 inches (159.3 mm) |
| **Body Font** | Times New Roman, 11 pt | Regular, 1.15 line spacing, 4 pt space-after, justified alignment |
| **Running Header** | Right-aligned 8.5 pt italic | `LINGUA-AUDIT: Auditing Information Inequality in Multilingual AI Systems` (suppressed on Page 1) |
| **Running Footer** | Centered 9.5 pt | Dynamic Word fields: `Page X of Y` |
| **Headings** | Strict academic hierarchy | H1: 13 pt Bold (13 pt before, 4 pt after, `keep_with_next`)<br>H2: 11.5 pt Bold (10 pt before, 3 pt after, `keep_with_next`)<br>H3: 11 pt Bold Italic (7 pt before, 2 pt after, `keep_with_next`) |
| **Figure 1** | Centered 300 DPI graphic | 6.20 inches wide with bold academic caption beneath |
| **Equations** | Formatted display tables | 2-column borderless layout: centered formula, right-aligned `(N)` tag (Eq. 1–8) |
| **Total Pages** | **14 pages** | Exactly within the target range of 12–15 pages |

---

## 3. Structural Section and Page Flow

The document cleanly partitions the research sections and appendices across exactly 14 pages:

1. **Pages 1–11: Main Manuscript**
   - Title, Author Metadata, Abstract, Scientific Disclosures, Keywords
   - Section 1: Introduction and Research Questions (RQ1–RQ4 grouped with Figure 1)
   - Section 2: Related Work (2.1–2.3)
   - Section 3: Benchmark Design and Task Construction (Table 1: Domain Distribution)
   - Section 4: Language Conditions and Model Configurations
   - Section 5: Data Collection and Reproducibility (Table 2: Execution Matrix)
   - Section 6: Metric Definitions and Scoring Protocol (Table 3: 13 Metrics Summary; Equations 2–6)
   - Section 7: Statistical Analysis Plan (Equations 7–8; GLMMs, CLMMs, Hurdle models, Holm correction on $m=9$)
   - Section 8: Benchmark and Software Verification Results (Diagnostics summary)
   - Section 9: Discussion (Methodological Governance, Quarantined Audit, Code-Switching)
   - Section 10: Limitations and Threats to Validity (Points 1–5)
   - Section 11: Ethics and Data Governance
   - Section 12: Conclusion and Future Work (Next steps: API collection, human calibration)
   - Reproducibility Statement
2. **Page 12: References**
   - Starts on a dedicated new page (`w:pageBreak`).
   - 17 IEEE-style bracketed entries (`[1]` through `[17]`) numbered by first appearance in text.
   - Hanging indent (0.35 in) with justified alignment.
3. **Page 13: Appendix A**
   - Starts on a dedicated new page (`w:pageBreak`).
   - Table A.1: Complete 13-Metric Implementation & Verification Inventory.
   - Restructured into 5 spacious columns to prevent word fragmentation or narrow column wrapping.
   - Full table (all 13 rows + footnotes) completely self-contained on Page 13.
4. **Page 14: Appendix B**
   - Starts on a dedicated new page (`w:pageBreak`).
   - Table B.1: Synthetic Fixture Diagnostic Characteristics Across Language Scaffolding.
   - Table B.2: Synthetic Fixture Script Composition Across Language Conditions.
   - Self-contained on Page 14 with unclipped headings and clean cell padding.

---

## 4. Academic Table Design & Fixes Applied

In accordance with preprint review guidelines, all tables were built as genuine, editable Word XML tables (`w:tbl`):

- **Booktabs Rule Styling:** Formatted with a 1 pt top border, a 0.75 pt header separator rule, and a 1 pt bottom border, omitting distracting vertical lines.
- **Header Shading:** Distinct `#F1F5F9` light slate fill for header cells.
- **Repeating Headers:** Every table incorporates `<w:tblHeader/>` on row 0 so that headers automatically repeat if imported into different page dimensions.
- **Row Anti-Split Protection:** Every row incorporates `<w:cantSplit/>` to prevent mid-row page splits.
- **Cell Padding:** Top/bottom padding of 25–50 dxa (1.25–2.5 pt) and left/right margins of 70–80 dxa (3.5–4.0 pt) ensure generous cell breathing room.
- **Word Fragmentation Prevention:** Column widths in Table 2, Table A.1, Table B.1, and Table B.2 were mathematically calibrated to the 6.27-inch printable margin. Narrow fragmented words (e.g., `UNVALI-DATED`, `Completenes-s`, `Latenc-y`) were completely eliminated.
- **No Stretched Justification:** Newlines within bullet and numbered lists were separated into distinct Word paragraphs with left alignment, preventing awkward stretched spaces across justified margins.

---

## 5. Scientific Integrity Disclosures Preserved

The document strictly preserves all methodological disclosures and scientific boundaries:

1. **Benchmark and Framework Paper:** The manuscript presents benchmark design, metric definitions, software verification, and a prespecified statistical analysis plan. It does not claim empirical ranking of live LLMs.
2. **5,400 Programmatic Software Fixtures:** The 5,400 records in the frozen dataset are deterministic synthetic fixtures instantiated in 0.150 seconds to verify pipeline data flow and factorial matrix completeness—not live model API outputs.
3. **Target Model Slots:** The four models (Gemini 3.5 Flash, GPT-4o, Claude 3.5 Sonnet, Llama 3.1 70B) represent architectural slots in the execution protocol; no external endpoints were queried.
4. **Quarantined Evaluator Artifacts:** Earlier synthetic evaluator-validation statistics (derived from cloned labels) remain quarantined and are disclosed as a cautionary example.
5. **13 Empirically Unvalidated Metrics:** All 13 metrics are verified by 115 passing tests for software execution correctness, but remain empirically unvalidated pending genuine bilingual human annotation.
6. **Internal Ground-Truth Curation:** Benchmark tasks and facts were curated internally from official departmental guidelines and have not been certified by an independent legal panel.
7. **Pending Institutional Ethics Review:** Institutional ethics committee approval remains pending, and no human annotators were recruited prior to approval.
8. **Zero Fitted Statistical Models:** No statistical models have been fitted to genuine response data; no odds ratios, variance components, or p-values are claimed.

---

## 6. Unresolved Issues and Author Review Items

| Item | Status | Action Required from Author |
| :--- | :--- | :--- |
| **Email Address** | Confirmed: `1by23is231@bmsit.in` | None required; institutional email successfully integrated on Page 1. |
| **ORCID** | Omitted | Add ORCID identifier beneath affiliation if desired. |
| **Target Journal / Venue Style** | Single-column venue-neutral preprint | If submitting to a venue with a mandatory template (e.g., IEEE Transactions two-column or Springer LNCS), apply that template after preprint posting. |
| **License Declaration** | CC-BY-NC 4.0 intended | Add formal `LICENSE` file to repository root upon public release. |

---

## 7. Verification Summary

- **Visual Page Inspection:** Rendered into 150 DPI PNGs (`rendered_pages/page_01.png`–`page_14.png`) and inspected.
- **Word COM Inspection:** Programmatically verified via Microsoft Word COM automation:
  - Document opened cleanly with zero XML corruption errors.
  - Page count: **14 pages**.
  - Word count: **5,341 words**.
  - Total tables: **14** (6 data tables + 8 equation layout tables).
  - All text is selectable and editable.
