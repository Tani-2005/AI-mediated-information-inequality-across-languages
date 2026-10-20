# LINGUA-AUDIT: LaTeX Preprint Source Package (Version 2)

**Final Publication-Quality Preprint with IEEE Reference Formatting, Compressed Narrative, and Reassessed Novelty**

---

## 1. Author and Affiliation Metadata

- **Author:** Tanya Deep (Sole Author)
- **Affiliation:** BMS Institute of Technology and Management, Bengaluru, India
- **Email:** `[author-email@institution.edu]` (Clearly marked placeholder in `main.tex`; repository git config records `tanyadeep1587@gmail.com` if preferred for preprint deposit)
- **ORCID:** Omitted (no verified ORCID registered in project)
- **Date:** October 2026

---

## 2. Package Manifest

| File | Description |
| :--- | :--- |
| **`main.tex`** | Complete, professionally typeset manuscript in single-column academic format (`article`, 11pt, A4 paper, 1-inch margins). Incorporates IEEE numeric citations (`\cite{...}` $\rightarrow$ `[1]`), streamlined narrative (~12--15 pages), and modular appendices for exhaustive diagnostic tables. |
| **`references.bib`** | Clean BibTeX bibliography containing 17 verified peer-reviewed and pre-print citations formatted for IEEEtran numeric bibliography style (`\bibliographystyle{IEEEtran}`). |
| **`NOVELTY_REVIEW.md`** | Comprehensive prior-work review and novelty assessment comparing LINGUA-AUDIT with contemporary benchmarks (CitizenQuery-UK, IndQA, IndicGenBench, Indic-QA, GLUECoS, MILU), featuring a comparative matrix, candidate claim classifications, and recommended bounded novelty formulations. |
| **`README.md`** | Source package documentation, compilation instructions, and Overleaf / HAL submission guide. |

---

## 3. Structural and Typesetting Improvements in Version 2

This revised preprint resolves all layout and formatting issues identified in prior drafts:
1. **IEEE Numbered Citation Style:** Configured with `\usepackage{cite}` and `\bibliographystyle{IEEEtran}` to render citations cleanly as numeric callouts (`[1]`, `[2]`, `[3]--[5]`) ordered by first appearance in text, strictly preserving the standard single-column `article` class.
2. **De-cluttering & Page Budget (Target 12--15 Pages):**
   - Main text focuses on core contributions: benchmark design, 13 operational metric formulas, prespecified statistical analysis plan, and methodological governance.
   - The exhaustive 8-column metric implementation inventory is placed in **Appendix A** (`longtable` with canonical page-breaking headers and footers).
   - Detailed text length diagnostics and Devanagari/Latin script breakdown tables are placed in **Appendix B**.
   - Redundant disclaimers and multi-sentence caveats repeated across multiple sections have been consolidated into cohesive explanations with clear internal cross-references.
3. **Table & Equation Width Safety:**
   - Table 1, Table 2 (Metric overview), Table 3 (Execution matrix), and Appendix tables have been completely restructured with `booktabs`, `tabularx`, and `makecell` to prevent text clipping, excessive vertical word stacking, or margin overflow on standard A4 paper.
   - All equations are formatted with standard math environments fitting within 1-inch margins.

---

## 4. Compilation Instructions

### Local Command Line Compilation (`pdflatex` + `bibtex`)

Run the following commands within the `paper/latex_preprint_v2/` directory:

```bash
pdflatex main.tex
bibtex main
pdflatex main.tex
pdflatex main.tex
```

### Automated Compilation (`latexmk`)

```bash
latexmk -pdf main.tex
```

---

## 5. Overleaf and HAL Submission Workflow

### Overleaf Setup
1. Compress the contents of this directory into a ZIP file:
   - On Windows PowerShell:
     ```powershell
     Compress-Archive -Path main.tex, references.bib, README.md, NOVELTY_REVIEW.md -DestinationPath lingua_audit_preprint_v2.zip
     ```
   - On Linux/macOS:
     ```bash
     zip -r lingua_audit_preprint_v2.zip main.tex references.bib README.md NOVELTY_REVIEW.md
     ```
2. Log into [Overleaf](https://www.overleaf.com), select **New Project** $\rightarrow$ **Upload Project**, and select `lingua_audit_preprint_v2.zip`.
3. In Overleaf Settings, verify:
   - **Compiler:** `pdfLaTeX`
   - **TeX Live version:** `2022` or later
   - **Main document:** `main.tex`
4. Click **Recompile**. The document will compile cleanly and output the publication-ready PDF.

### HAL Archive Deposit ([hal.science](https://hal.science/))
1. Prepare a `.tar.gz` or `.zip` containing `main.tex` and `references.bib`.
2. Upload the archive under the **Document** tab on HAL.
3. Select `main.tex` as the primary file; HAL's automated server toolchain will compile the PDF and index the bibliography.
