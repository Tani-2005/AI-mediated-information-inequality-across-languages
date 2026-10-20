# LINGUA-AUDIT: LaTeX Preprint Source Package

This directory contains the complete, self-contained, publication-quality LaTeX preprint source package for:

> **LINGUA-AUDIT: A Reproducible Framework for Auditing Information Inequality in Multilingual AI Systems**

---

## 1. Author and Affiliation Metadata

- **Author:** Tanya Deep (Sole Author)
- **Affiliation:** BMS Institute of Technology and Management, Bengaluru, India
- **Email:** `[author-email@institution.edu]` (Placeholder in `main.tex`; repository git config records `tanyadeep1587@gmail.com` if preferred for preprint deposit)
- **ORCID:** Omitted (no verified ORCID registered in project)
- **Date:** October 2026

---

## 2. Source Package Manifest

| File | Description |
| :--- | :--- |
| `main.tex` | Complete manuscript in venue-neutral, single-column academic format (`article`, 11pt, A4 paper, 1-inch margins). |
| `references.bib` | Clean BibTeX bibliography containing all 13 cited peer-reviewed works with verified citation keys. |
| `README.md` | Compilation instructions, package manifest, and HAL submission guide. |

---

## 3. Compilation Instructions

The document is designed to compile cleanly using standard, unmodified TeX Live (2020 or later), MacTeX, or MiKTeX distributions without requiring specialized fonts, shell-escape, or external services.

### Standard Command-Line Compilation (`pdflatex` + `bibtex`)

Run the following commands in the `paper/latex_preprint/` directory:

```bash
pdflatex main.tex
bibtex main
pdflatex main.tex
pdflatex main.tex
```

### Automated Compilation (`latexmk`)

Alternatively, compile in a single command using `latexmk`:

```bash
latexmk -pdf main.tex
```

To clean intermediate auxiliary files (`.aux`, `.bbl`, `.blg`, `.log`, `.out`):

```bash
latexmk -c
```

---

## 4. HAL Submission Guide

This package is prepared specifically for deposit in the **HAL Open Science Archive** (Hyper Articles en Ligne, [hal.science](https://hal.science/)):

1. **Archive Preparation:** Compress the contents of this directory into a `.zip` or `.tar.gz` archive:
   ```bash
   tar -czvf lingua_audit_hal_source.tar.gz main.tex references.bib
   ```
2. **Master File Selection:** In the HAL submission interface, designate `main.tex` as the primary (master) file.
3. **TeX Engine:** HAL will compile the source automatically using its standard Linux `pdflatex` + `bibtex` workflow.
4. **Standard Dependencies:** All included packages are standard TeX Live components:
   - `geometry` (margins and A4 layout)
   - `inputenc`, `fontenc` (UTF-8 / T1 encoding)
   - `amsmath`, `amssymb`, `amsfonts` (mathematical typesetting)
   - `booktabs`, `tabularx`, `longtable`, `array`, `makecell` (tables)
   - `natbib` (author--year citations)
   - `microtype` (typographic refinement)
   - `fancyvrb`, `url`, `hyperref` (formatting and hyperlinks)

---

## 5. Scientific Disclosures and Content Preservation

This LaTeX preprint directly translates the finalized, verified manuscript `paper/LINGUA_AUDIT_manuscript_draft.md`:
- **Paper Type:** Benchmark-design, measurement-specification, and reproducibility-framework paper.
- **Fixture Disclosure:** The 5,400 dataset responses are disclosed as deterministic baseline fixtures for software pipeline verification, not live model outputs.
- **Model Slots:** The four models (`gemini-3.5-flash`, `gpt-4o`, `claude-3.5-sonnet`, `llama-3.1-70b`) are specified as architectural target slots.
- **Quarantined Evaluator Data:** Invalid synthetic evaluator statistics from prior iterations remain quarantined and completely excluded.
- **Statistical Analysis Plan:** Specifies pooled population language main effects ($m=9$ tests) under Holm--Bonferroni correction ($\alpha=0.05$); zero models are presented as fitted to empirical data.
- **Tables and Figures:** All five benchmark tables (Tables 1--5) and the conceptual framework architecture diagram (Figure 1) are preserved in native LaTeX formatting.
