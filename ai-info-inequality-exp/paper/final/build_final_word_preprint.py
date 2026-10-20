import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import parse_xml, OxmlElement
from docx.oxml.ns import nsdecls, qn
import os

def create_document():
    doc = docx.Document()
    
    # 1. Page Setup: A4, 1-inch margins (210 mm x 297 mm; printable width = 6.27 in)
    section = doc.sections[0]
    section.page_width = Inches(8.27)   # 210 mm
    section.page_height = Inches(11.69) # 297 mm
    section.top_margin = Inches(1.0)
    section.bottom_margin = Inches(1.0)
    section.left_margin = Inches(1.0)
    section.right_margin = Inches(1.0)
    section.different_first_page_header_footer = True
    
    # 2. Header and Footer
    # Header on subsequent pages
    header = section.header
    p_head = header.paragraphs[0]
    p_head.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    run_head = p_head.add_run("LINGUA-AUDIT: Auditing Information Inequality in Multilingual AI Systems")
    run_head.font.name = "Times New Roman"
    run_head.font.size = Pt(8.5)
    run_head.font.italic = True
    run_head.font.color.rgb = RGBColor(100, 116, 139)
    
    # Footer on all pages: Centered Page Number
    def add_page_number(run):
        fldSimple = parse_xml(r'<w:fldSimple %s w:instr="PAGE"/>' % nsdecls('w'))
        run._r.append(fldSimple)

    def add_total_pages(run):
        fldSimple = parse_xml(r'<w:fldSimple %s w:instr="NUMPAGES"/>' % nsdecls('w'))
        run._r.append(fldSimple)

    # Footer subsequent
    footer = section.footer
    p_foot = footer.paragraphs[0]
    p_foot.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_foot1 = p_foot.add_run("Page ")
    r_foot1.font.name = "Times New Roman"
    r_foot1.font.size = Pt(9.5)
    r_foot1.font.color.rgb = RGBColor(100, 116, 139)
    add_page_number(r_foot1)
    r_foot2 = p_foot.add_run(" of ")
    r_foot2.font.name = "Times New Roman"
    r_foot2.font.size = Pt(9.5)
    r_foot2.font.color.rgb = RGBColor(100, 116, 139)
    add_total_pages(r_foot2)
    
    # Footer first page
    first_footer = section.first_page_footer
    p_ffoot = first_footer.paragraphs[0]
    p_ffoot.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_ff1 = p_ffoot.add_run("Page ")
    r_ff1.font.name = "Times New Roman"
    r_ff1.font.size = Pt(9.5)
    r_ff1.font.color.rgb = RGBColor(100, 116, 139)
    add_page_number(r_ff1)
    r_ff2 = p_ffoot.add_run(" of ")
    r_ff2.font.name = "Times New Roman"
    r_ff2.font.size = Pt(9.5)
    r_ff2.font.color.rgb = RGBColor(100, 116, 139)
    add_total_pages(r_ff2)

    # Set default style
    normal_style = doc.styles['Normal']
    normal_style.font.name = 'Times New Roman'
    normal_style.font.size = Pt(11)
    normal_style.font.color.rgb = RGBColor(17, 24, 39)
    normal_style.paragraph_format.line_spacing = 1.15
    normal_style.paragraph_format.space_after = Pt(4)
    normal_style.paragraph_format.space_before = Pt(0)
    normal_style.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY

    # Formatting Helpers
    def add_p(text, bold_prefix=None, space_after=4, space_before=0, align=WD_ALIGN_PARAGRAPH.JUSTIFY, italic=False, keep_with_next=False):
        p = doc.add_paragraph()
        p.alignment = align
        p.paragraph_format.space_after = Pt(space_after)
        p.paragraph_format.space_before = Pt(space_before)
        p.paragraph_format.line_spacing = 1.15
        p.paragraph_format.keep_with_next = keep_with_next
        if bold_prefix:
            r_b = p.add_run(bold_prefix)
            r_b.bold = True
            r_b.font.name = 'Times New Roman'
            r_b.font.size = Pt(11)
        if text:
            r = p.add_run(text)
            r.font.name = 'Times New Roman'
            r.font.size = Pt(11)
            r.italic = italic
        return p

    def add_bullet(text, bold_prefix=None, space_after=3, keep_with_next=False, align=WD_ALIGN_PARAGRAPH.LEFT):
        p = doc.add_paragraph()
        p.alignment = align
        p.paragraph_format.left_indent = Inches(0.25)
        p.paragraph_format.first_line_indent = Inches(-0.25)
        p.paragraph_format.space_before = Pt(0)
        p.paragraph_format.space_after = Pt(space_after)
        p.paragraph_format.line_spacing = 1.15
        p.paragraph_format.keep_with_next = keep_with_next
        
        r_bullet = p.add_run("• ")
        r_bullet.bold = True
        r_bullet.font.name = 'Times New Roman'
        r_bullet.font.size = Pt(11)
        
        if bold_prefix:
            r_b = p.add_run(bold_prefix)
            r_b.bold = True
            r_b.font.name = 'Times New Roman'
            r_b.font.size = Pt(11)
        if text:
            r = p.add_run(text)
            r.font.name = 'Times New Roman'
            r.font.size = Pt(11)
        return p

    def add_numbered(num_str, text, bold_prefix=None, space_after=3, keep_with_next=False, align=WD_ALIGN_PARAGRAPH.LEFT):
        p = doc.add_paragraph()
        p.alignment = align
        p.paragraph_format.left_indent = Inches(0.3)
        p.paragraph_format.first_line_indent = Inches(-0.3)
        p.paragraph_format.space_before = Pt(0)
        p.paragraph_format.space_after = Pt(space_after)
        p.paragraph_format.line_spacing = 1.15
        p.paragraph_format.keep_with_next = keep_with_next
        
        r_num = p.add_run(num_str + " ")
        r_num.bold = True
        r_num.font.name = 'Times New Roman'
        r_num.font.size = Pt(11)
        
        if bold_prefix:
            r_b = p.add_run(bold_prefix)
            r_b.bold = True
            r_b.font.name = 'Times New Roman'
            r_b.font.size = Pt(11)
        if text:
            r = p.add_run(text)
            r.font.name = 'Times New Roman'
            r.font.size = Pt(11)
        return p

    def add_h1(text):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(13)
        p.paragraph_format.space_after = Pt(4)
        p.paragraph_format.keep_with_next = True
        r = p.add_run(text)
        r.font.name = 'Times New Roman'
        r.font.size = Pt(13)
        r.bold = True
        r.font.color.rgb = RGBColor(15, 23, 42)
        return p

    def add_h2(text):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(10)
        p.paragraph_format.space_after = Pt(3)
        p.paragraph_format.keep_with_next = True
        r = p.add_run(text)
        r.font.name = 'Times New Roman'
        r.font.size = Pt(11.5)
        r.bold = True
        r.font.color.rgb = RGBColor(30, 41, 59)
        return p

    def add_h3(text):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(7)
        p.paragraph_format.space_after = Pt(2)
        p.paragraph_format.keep_with_next = True
        r = p.add_run(text)
        r.font.name = 'Times New Roman'
        r.font.size = Pt(11)
        r.bold = True
        r.italic = True
        r.font.color.rgb = RGBColor(51, 65, 85)
        return p

    def add_equation(eq_text, eq_num):
        t = doc.add_table(rows=1, cols=2)
        t.alignment = WD_TABLE_ALIGNMENT.CENTER
        t.autofit = False
        t.columns[0].width = Inches(5.5)
        t.columns[1].width = Inches(0.77)
        
        tblPr = t._tbl.tblPr
        tblPr.append(parse_xml(
            r'<w:tblBorders %s><w:top w:val="none"/><w:left w:val="none"/><w:bottom w:val="none"/><w:right w:val="none"/><w:insideH w:val="none"/><w:insideV w:val="none"/></w:tblBorders>' % nsdecls('w')
        ))
        row = t.rows[0]
        row._tr.get_or_add_trPr().append(parse_xml(r'<w:cantSplit %s/>' % nsdecls('w')))
        
        c0 = row.cells[0]
        c0.width = Inches(5.5)
        p0 = c0.paragraphs[0]
        p0.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p0.paragraph_format.space_before = Pt(3)
        p0.paragraph_format.space_after = Pt(3)
        r0 = p0.add_run(eq_text)
        r0.font.name = 'Times New Roman'
        r0.font.size = Pt(11)
        r0.italic = True
        
        c1 = row.cells[1]
        c1.width = Inches(0.77)
        p1 = c1.paragraphs[0]
        p1.alignment = WD_ALIGN_PARAGRAPH.RIGHT
        p1.paragraph_format.space_before = Pt(3)
        p1.paragraph_format.space_after = Pt(3)
        r1 = p1.add_run(f"({eq_num})")
        r1.font.name = 'Times New Roman'
        r1.font.size = Pt(11)
        
        p_after = doc.add_paragraph()
        p_after.paragraph_format.space_before = Pt(0)
        p_after.paragraph_format.space_after = Pt(3)

    def style_table(table, col_widths, alignments, font_size_pt=9.0, cell_pad_v=50):
        table.alignment = WD_TABLE_ALIGNMENT.CENTER
        table.autofit = False
        tblPr = table._tbl.tblPr
        
        # Booktabs borders: Top 8 (1pt), Bottom 8 (1pt), no vertical lines
        borders = parse_xml(
            r'<w:tblBorders %s>'
            r'<w:top w:val="single" w:sz="8" w:space="0" w:color="1E293B"/>'
            r'<w:bottom w:val="single" w:sz="8" w:space="0" w:color="1E293B"/>'
            r'<w:insideH w:val="none"/>'
            r'<w:left w:val="none"/>'
            r'<w:right w:val="none"/>'
            r'<w:insideV w:val="none"/>'
            r'</w:tblBorders>' % nsdecls('w')
        )
        tblPr.append(borders)
        
        # Cell padding
        padding = parse_xml(
            r'<w:tblCellMar %s>'
            r'<w:top w:w="%d" w:type="dxa"/>'
            r'<w:bottom w:w="%d" w:type="dxa"/>'
            r'<w:left w:w="70" w:type="dxa"/>'
            r'<w:right w:w="70" w:type="dxa"/>'
            r'</w:tblCellMar>' % (nsdecls('w'), cell_pad_v, cell_pad_v)
        )
        tblPr.append(padding)
        
        for r_idx, row in enumerate(table.rows):
            trPr = row._tr.get_or_add_trPr()
            trPr.append(parse_xml(r'<w:cantSplit %s/>' % nsdecls('w')))
            if r_idx == 0:
                trPr.append(parse_xml(r'<w:tblHeader %s/>' % nsdecls('w')))
                
            for c_idx, cell in enumerate(row.cells):
                cell.width = col_widths[c_idx]
                p = cell.paragraphs[0]
                p.alignment = alignments[c_idx]
                p.paragraph_format.space_before = Pt(1.0)
                p.paragraph_format.space_after = Pt(1.0)
                p.paragraph_format.line_spacing = 1.05
                
                # Header row styling
                if r_idx == 0:
                    tcPr = cell._tc.get_or_add_tcPr()
                    tcPr.append(parse_xml(r'<w:shd %s w:fill="F1F5F9"/>' % nsdecls('w')))
                    tcPr.append(parse_xml(r'<w:tcBorders %s><w:bottom w:val="single" w:sz="6" w:color="334155"/></w:tcBorders>' % nsdecls('w')))
                    for run in p.runs:
                        run.font.name = 'Times New Roman'
                        run.font.size = Pt(font_size_pt)
                        run.bold = True
                        run.font.color.rgb = RGBColor(15, 23, 42)
                else:
                    for run in p.runs:
                        run.font.name = 'Times New Roman'
                        run.font.size = Pt(font_size_pt)

    def add_table_caption(text):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(9)
        p.paragraph_format.space_after = Pt(3)
        p.paragraph_format.keep_with_next = True
        r = p.add_run(text)
        r.font.name = 'Times New Roman'
        r.font.size = Pt(10)
        r.bold = True
        r.font.color.rgb = RGBColor(15, 23, 42)
        return p

    def add_figure_caption(text):
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.paragraph_format.space_before = Pt(4)
        p.paragraph_format.space_after = Pt(9)
        r = p.add_run(text)
        r.font.name = 'Times New Roman'
        r.font.size = Pt(9.5)
        r.bold = True
        r.font.color.rgb = RGBColor(30, 41, 59)
        return p

    # =========================================================================
    # TITLE & AUTHOR BLOCK
    # =========================================================================
    p_title = doc.add_paragraph()
    p_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_title.paragraph_format.space_before = Pt(4)
    p_title.paragraph_format.space_after = Pt(8)
    r_title = p_title.add_run("LINGUA-AUDIT: Auditing Information Inequality in Multilingual AI Systems")
    r_title.font.name = "Times New Roman"
    r_title.font.size = Pt(16.5)
    r_title.bold = True
    r_title.font.color.rgb = RGBColor(15, 23, 42)

    p_auth = doc.add_paragraph()
    p_auth.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_auth.paragraph_format.space_before = Pt(0)
    p_auth.paragraph_format.space_after = Pt(2)
    r_auth = p_auth.add_run("Tanya Deep")
    r_auth.font.name = "Times New Roman"
    r_auth.font.size = Pt(12)
    r_auth.bold = True

    p_aff = doc.add_paragraph()
    p_aff.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_aff.paragraph_format.space_before = Pt(0)
    p_aff.paragraph_format.space_after = Pt(2)
    r_aff = p_aff.add_run("BMS Institute of Technology and Management, Bengaluru, India")
    r_aff.font.name = "Times New Roman"
    r_aff.font.size = Pt(10)
    r_aff.font.color.rgb = RGBColor(71, 85, 105)

    p_email = doc.add_paragraph()
    p_email.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_email.paragraph_format.space_before = Pt(0)
    p_email.paragraph_format.space_after = Pt(10)
    r_email = p_email.add_run("1by23is231@bmsit.in")
    r_email.font.name = "Times New Roman"
    r_email.font.size = Pt(9.5)
    r_email.font.color.rgb = RGBColor(100, 116, 139)

    # =========================================================================
    # ABSTRACT & KEYWORDS BLOCK
    # =========================================================================
    p_abs1 = doc.add_paragraph()
    p_abs1.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    p_abs1.paragraph_format.left_indent = Inches(0.35)
    p_abs1.paragraph_format.right_indent = Inches(0.35)
    p_abs1.paragraph_format.space_after = Pt(4)
    r_absh = p_abs1.add_run("Abstract—")
    r_absh.font.name = "Times New Roman"
    r_absh.font.size = Pt(10)
    r_absh.bold = True
    r_abst1 = p_abs1.add_run(
        "As large language models (LLMs) are increasingly proposed as conversational intermediaries for public services, civic welfare schemes, and statutory entitlements, information inequality across linguistic communities has emerged as an urgent technical and societal challenge. In multilingual societies, performance disparities do not merely reflect stylistic variations or fluency degradation; they threaten to manifest as substantive information inequality, wherein citizens querying administrative systems in non-English or code-switched vernaculars receive incomplete, outdated, or factually erroneous guidance."
    )
    r_abst1.font.name = "Times New Roman"
    r_abst1.font.size = Pt(10)

    p_abs2 = doc.add_paragraph()
    p_abs2.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    p_abs2.paragraph_format.left_indent = Inches(0.35)
    p_abs2.paragraph_format.right_indent = Inches(0.35)
    p_abs2.paragraph_format.space_after = Pt(4)
    r_abst2 = p_abs2.add_run(
        "This paper presents LINGUA-AUDIT, an open, reproducible civic-information benchmark design, measurement protocol, and auditing framework created to systematically evaluate substantive information inequality in multilingual AI systems. Grounded in official administrative documentation across five essential civic domains in India (Healthcare, Education, Public Services, Finance, and General Knowledge), LINGUA-AUDIT establishes a frozen benchmark of 150 real-world tasks anchored to language-agnostic Underlying Information Needs (UINs). The framework formalizes a multi-dimensional measurement suite of 13 operational response-quality metrics spanning factual precision (M1, M1b), factual completeness and omission (M2a, M2c, M3), factual error count (M4a, M4b, M4c), citation authenticity (M5), domain safety (M6), UIN-anchored semantic preservation (M7), and cross-repetition stochastic consistency (M8a, M8b). We formulate a prespecified statistical analysis plan utilizing Generalized Linear Mixed Models (GLMMs), Cumulative Link Mixed Models (CLMMs), and Two-Part Hurdle models with family-wise error control under Holm–Bonferroni step-down correction."
    )
    r_abst2.font.name = "Times New Roman"
    r_abst2.font.size = Pt(10)

    p_abs3 = doc.add_paragraph()
    p_abs3.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    p_abs3.paragraph_format.left_indent = Inches(0.35)
    p_abs3.paragraph_format.right_indent = Inches(0.35)
    p_abs3.paragraph_format.space_after = Pt(4)
    r_abst3 = p_abs3.add_run(
        "The software pipeline and end-to-end data flow are verified across a complete factorial matrix of 150 tasks × 3 language conditions (English, Hindi, Hinglish) × 4 target model slots × 3 repetitions = 5,400 factorial cells, supported by 115 passing unit and regression tests."
    )
    r_abst3.font.name = "Times New Roman"
    r_abst3.font.size = Pt(10)

    # Disclosures
    p_disc = doc.add_paragraph()
    p_disc.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    p_disc.paragraph_format.left_indent = Inches(0.35)
    p_disc.paragraph_format.right_indent = Inches(0.35)
    p_disc.paragraph_format.space_after = Pt(4)
    r_disch = p_disc.add_run("Scientific and Validation Disclosures: ")
    r_disch.bold = True
    r_disch.font.name = "Times New Roman"
    r_disch.font.size = Pt(9.5)
    r_disct = p_disc.add_run(
        "(1) Framework Scope: This manuscript presents a benchmark-design and reproducibility framework; it does not report empirical comparisons or rankings of live LLMs. "
        "(2) Software Verification Fixtures: The 5,400 records in the dataset are deterministic, programmatic baseline fixtures instantiated to verify schema compliance and pipeline integrity—not genuine outputs from commercial model endpoints. "
        "(3) Pending Evaluator Validation: A prior automated evaluator validation was found to rely on cloned synthetic references and was quarantined. All 13 quality metrics remain empirically unvalidated pending genuine bilingual human annotation. "
        "(4) Pre-Registration Gate: Live model API execution (data collection) and human evaluator calibration (measurement validation) represent separate future activities that precede downstream empirical estimation."
    )
    r_disct.font.name = "Times New Roman"
    r_disct.font.size = Pt(9.5)

    # Keywords
    p_kw = doc.add_paragraph()
    p_kw.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    p_kw.paragraph_format.left_indent = Inches(0.35)
    p_kw.paragraph_format.right_indent = Inches(0.35)
    p_kw.paragraph_format.space_after = Pt(12)
    r_kwh = p_kw.add_run("Keywords—")
    r_kwh.bold = True
    r_kwh.font.name = "Times New Roman"
    r_kwh.font.size = Pt(10)
    r_kwt = p_kw.add_run("Information Inequality, Multilingual Benchmark Design, Auditing Framework, LLM Evaluation, Code-Switching, Algorithmic Governance, Statutory Ground Truth, Reproducibility.")
    r_kwt.font.name = "Times New Roman"
    r_kwt.font.size = Pt(10)

    # =========================================================================
    # 1. INTRODUCTION AND RESEARCH QUESTIONS
    # =========================================================================
    add_h1("1. Introduction and Research Questions")
    add_p(
        "Large language models (LLMs) are transitioning from research prototypes into citizen-facing conversational interfaces. Across developing and linguistically diverse nations, public agencies and civic organizations are exploring generative AI to automate citizen advisory services: explaining welfare eligibility, detailing statutory identity documentation workflows, and clarifying public health mandates. In these high-stakes civic contexts, user populations are frequently socioeconomically vulnerable and linguistically diverse, relying on automated systems for actionable, life-critical guidance."
    )
    add_p(
        "Despite rapid advances in multilingual natural language processing, frontier generative models exhibit profound disparities across languages. Existing multilingual evaluations have predominantly focused on surface-level capabilities: cross-lingual perplexity, translation BLEU/ChrF scores, or multiple-choice academic examinations [1], [2]. While valuable for measuring broad capability, these evaluations do not assess whether models satisfy identical civic information needs equitably across languages: they do not measure information inequality."
    )

    add_h2("1.1 Defining AI-Mediated Information Inequality")
    add_p("We define AI-mediated information inequality as:")
    p_quote = doc.add_paragraph()
    p_quote.paragraph_format.left_indent = Inches(0.4)
    p_quote.paragraph_format.right_indent = Inches(0.4)
    p_quote.paragraph_format.space_before = Pt(3)
    p_quote.paragraph_format.space_after = Pt(5)
    r_q = p_quote.add_run("“The systematic divergence in the substantive, factual, and actionable information provided to citizens seeking to satisfy identical information needs across different linguistic conditions.”")
    r_q.bold = True
    r_q.font.name = "Times New Roman"
    r_q.font.size = Pt(10.5)

    add_p(
        "In public administrative systems, information inequality creates tangible, asymmetric harms. If an English query regarding maternal health benefits yields accurate income thresholds, mandatory document lists, and links to the official portal, while an equivalent Hindi or code-switched Hinglish query yields outdated financial caps, omits mandatory attestation steps, or provides hallucinated URLs, information inequality has occurred. The non-English speaker faces administrative disqualification, missed entitlement deadlines, or economic loss—despite asking the same statutory question."
    )

    # Insert Figure 1
    fig_path = "paper/final/figure1_framework_overview.png"
    if os.path.exists(fig_path):
        p_fig = doc.add_paragraph()
        p_fig.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_fig.paragraph_format.space_before = Pt(8)
        p_fig.paragraph_format.space_after = Pt(2)
        p_fig.paragraph_format.keep_with_next = True
        p_fig.add_run().add_picture(fig_path, width=Inches(6.2))
        add_figure_caption("Figure 1: Conceptual workflow of the LINGUA-AUDIT framework. Statutory authorities anchor 150 civic tasks across five domains. Each task is operationalized across three language conditions and four target model slots over three repetitions (N = 5,400 factorial cells). Responses are evaluated across 13 operational metrics once evaluator calibration is completed.")

    add_h2("1.2 Research Questions Prespecified by the Framework")
    add_p(
        "The framework provides the measurement methodology and statistical architecture needed to answer four foundational research questions once live models are evaluated:",
        keep_with_next=True
    )
    add_bullet(
        " Does the coverage of statutory Critical Facts (M2a) and the omission rate of mandatory prerequisites (M3) differ significantly between English, Hindi, and Hinglish queries when adjusting for model family and task domain?",
        bold_prefix="RQ1 (Completeness & Omission Disparity):",
        keep_with_next=True
    )
    add_bullet(
        " Are vernacular and code-switched queries subject to significantly higher factual contradiction rates (M4a, M4c) and depressed precision (M1, M1b) against statutory ground truth compared to English queries?",
        bold_prefix="RQ2 (Factual Precision & Contradiction Severity):",
        keep_with_next=True
    )
    add_bullet(
        " Do models exhibit elevated rates of hallucinated or non-authoritative URL citations (M5) and increased citizen administrative/medical risk levels (M6) in vernacular and code-switched interactions?",
        bold_prefix="RQ3 (Citation Authenticity & Citizen Risk):",
        keep_with_next=True
    )
    add_bullet(
        " Is information delivery in vernacular queries less stochastically stable across repeated generations, as quantified by completeness variance (M8a) and Critical Fact Jaccard concordance (M8b)?",
        bold_prefix="RQ4 (Stochastic Repetition Consistency):",
        keep_with_next=False
    )

    add_h2("1.3 Scope and Contributions of this Manuscript")
    add_p("This manuscript presents a benchmark-design, measurement-specification, and reproducibility framework; it is not an empirical model-comparison study. Our core contributions are:")
    add_numbered(
        "1.",
        " A curated benchmark of 150 administrative tasks across 5 societal domains in India, grounded in official regulatory guidelines and indexed by language-agnostic Underlying Information Needs (UINs).",
        bold_prefix="Civic-Information Benchmark Design:"
    )
    add_numbered(
        "2.",
        " Mathematical specifications for 13 response-quality metrics spanning factual precision, coverage, omission, error deduplication, citation quality, safety, and cross-repetition consistency.",
        bold_prefix="Multi-Dimensional Operational Metrics:"
    )
    add_numbered(
        "3.",
        " A pre-registered modeling framework using Binomial GLMMs, Negative Binomial GLMMs, CLMMs, and Two-Part Hurdle models with family-wise error rate control on a designated confirmatory family (m = 9 tests).",
        bold_prefix="Prespecified Statistical Analysis Plan:"
    )
    add_numbered(
        "4.",
        " An open-source Python scoring architecture verified by 115 passing tests against a 5,400-cell factorial software fixture matrix.",
        bold_prefix="Reproducible Software Pipeline:"
    )
    add_numbered(
        "5.",
        " Explicit quarantine of invalid prior synthetic evaluator validation artifacts, clear separation of software correctness from empirical construct validity, and transparent disclosure of pending validation steps.",
        bold_prefix="Methodological Governance:"
    )

    # =========================================================================
    # 2. RELATED WORK
    # =========================================================================
    add_h1("2. Related Work")
    add_h2("2.1 Multilingual NLP and Resource Asymmetries")
    add_p(
        "Disparities in natural language processing across languages are well-documented. Blasi et al. [3] established that NLP development correlates with national wealth and digital web text availability rather than speaker population. Joshi et al. [4] highlighted that despite over 600 million speakers, Hindi remains digitally under-resourced relative to its demographic size due to uncurated web crawls and limited parallel resources. Bender et al. [5] observed that models trained on massive, uncurated web data amplify dominant cultural norms while degrading in low-resource and vernacular contexts."
    )

    add_h2("2.2 Multilingual Generative Benchmarks")
    add_p(
        "Early multilingual benchmarks relied heavily on direct translations of English corpora, such as XNLI [2], TyDi QA [6], and multilingual MMLU [1]. However, as Ahuja et al. [7] and Bang et al. [8] demonstrated, translated benchmarks suffer from “translationese” and cultural disconnects, failing to test authentic localized problem-solving."
    )
    add_p(
        "Recent efforts have expanded Indic language evaluation. Singh et al. [9] introduced IndicGenBench to benchmark generative capabilities across 29 Indic languages on classic NLP tasks. Singh et al. [10] developed INDIC QA BENCHMARK for context-grounded reading comprehension across 11 Indian languages. In parallel, OpenAI [11] released IndQA to evaluate cultural fluency and regional reasoning across 12 Indian languages and Hinglish. In the public sector, Majithia et al. [12] introduced CitizenQuery, benchmarking LLM factuality and abstention on UK government services (gov.uk) in English."
    )
    add_p(
        "LINGUA-AUDIT addresses a distinct intersection: auditing cross-lingual information inequality in statutory civic administration. While CitizenQuery focuses on monolingual UK English services, and IndQA/IndicGenBench evaluate broad cultural or linguistic capabilities, LINGUA-AUDIT evaluates whether identical administrative entitlements in India are delivered equitably across English, Devanagari Hindi, and Romanized code-switching. Building on GLUECoS [13], which established code-switching evaluation for standard NLP tasks, LINGUA-AUDIT treats Hindi-English code-switching as a primary communicative condition for civic service navigation."
    )

    add_h2("2.3 Automated Factual Evaluation and Evaluator Reliability")
    add_p(
        "Evaluating factual precision in generative text has inspired frameworks like FActScore [14] and HELM [15]. However, when LLMs serve as evaluators (“LLM-as-a-judge” [16]), severe leniency bias and script-dependent degradation arise [17]. Crucially, validating automated evaluators against synthetic model outputs rather than human ground truth creates circular self-validation. LINGUA-AUDIT enforces strict methodological governance by anchoring facts to statutory documentation and isolating uncalibrated metrics pending independent human annotation."
    )

    # =========================================================================
    # 3. BENCHMARK DESIGN AND TASK CONSTRUCTION
    # =========================================================================
    add_h1("3. Benchmark Design and Task Construction")
    add_h2("3.1 Domain Architecture and Civic Selection")
    add_p(
        "The benchmark comprises 150 administrative and civic tasks representing critical daily interactions between citizens and public institutions in India, equally partitioned across five societal domains (N = 30 per domain; Table 1):"
    )
    add_numbered("1.", " Entitlements under public health insurance (PM-JAY), universal immunization schedules, revised tuberculosis treatment notification rules, public hospital emergency mandates, and subsidized medicine dispensaries.", bold_prefix="Healthcare (N=30):")
    add_numbered("2.", " Quota admissions under RTE Act Section 12(1)(c), National Scholarship Portal rules, university reservations, vocational skill certification, and exam fee waivers.", bold_prefix="Education (N=30):")
    add_numbered("3.", " Mandatory documentation for Aadhaar demographic/biometric updates, Voter ID registration, ration card portability (ONORC), passport police verification, and municipal grievance filings.", bold_prefix="Public Services (N=30):")
    add_numbered("4.", " PM-KISAN direct benefit transfers, Atal Pension Yojana micro-pensions, Mudra microenterprise loans, small savings tax exemption schemes, and banking ombudsman disputes.", bold_prefix="Finance (N=30):")
    add_numbered("5.", " Statutory procedures under RTI Act 2005, Consumer Protection Act 2019 filings, citizen rights during police encounters, and public service guarantee acts.", bold_prefix="General Knowledge & Civic Rights (N=30):")
    add_p(
        "Tasks reflect balanced administrative complexity: 66 Moderate (44.0%), 48 Low (32.0%), and 36 High difficulty (24.0%); 60 High (40.0%), 60 Moderate (40.0%), and 30 Low safety sensitivity (20.0%)."
    )

    # Table 1
    add_table_caption("Table 1: Benchmark task and ground-truth distribution across the five civic domains.")
    t1 = doc.add_table(rows=7, cols=7)
    t1_headers = ["Civic Domain", "Tasks (N=150)", "Critical Facts (CF)", "Important Facts (IF)", "Primary Sources", "Mod./High Difficulty", "High Safety Sensitivity"]
    for c_i, h in enumerate(t1_headers):
        t1.rows[0].cells[c_i].paragraphs[0].text = h
    t1_data = [
        ["Healthcare", "30", "90", "60", "30", "24 (80.0%)", "22 (73.3%)"],
        ["Education", "30", "90", "60", "30", "18 (60.0%)", "8 (26.7%)"],
        ["Public Services", "30", "90", "60", "30", "22 (73.3%)", "12 (40.0%)"],
        ["Finance", "30", "90", "60", "30", "22 (73.3%)", "14 (46.7%)"],
        ["General Knowledge", "30", "90", "60", "30", "16 (53.3%)", "4 (13.3%)"],
        ["Total / Overall", "150", "450", "300", "150", "102 (68.0%)", "60 (40.0%)"]
    ]
    for r_i, row in enumerate(t1_data):
        for c_i, val in enumerate(row):
            t1.rows[r_i+1].cells[c_i].paragraphs[0].text = val
    t1_widths = [Inches(1.4), Inches(0.75), Inches(0.8), Inches(0.8), Inches(0.75), Inches(0.9), Inches(0.87)]
    t1_aligns = [WD_ALIGN_PARAGRAPH.LEFT, WD_ALIGN_PARAGRAPH.CENTER, WD_ALIGN_PARAGRAPH.CENTER, WD_ALIGN_PARAGRAPH.CENTER, WD_ALIGN_PARAGRAPH.CENTER, WD_ALIGN_PARAGRAPH.CENTER, WD_ALIGN_PARAGRAPH.CENTER]
    style_table(t1, t1_widths, t1_aligns)

    add_h2("3.2 Statutory Ground Truth Anchoring and Curation Scope")
    add_p(
        "Every task in LINGUA-AUDIT is grounded in public statutory authorities recorded in the master task registry (master_task_registry_150.json):"
    )
    add_bullet(" Sourced from official guidelines, gazette notifications, ministry circulars, and departmental domains across 25 administrative bodies. Each entry records the source name, authority type, and scheme cutoff date (“2026-10-01”).", bold_prefix="Primary Statutory Authorities (N=150):")
    add_bullet(" Mandatory statutory criteria without which a citizen cannot access the service (e.g., income ceilings, identity proofs, filing deadlines).", bold_prefix="Critical Facts (CF; N=450, exactly 3/task):")
    add_bullet(" Essential procedural context (e.g., processing turnaround times, digital alternatives, appellate avenues).", bold_prefix="Important Facts (IF; N=300, exactly 2/task):")
    add_bullet(" Explicit boundaries to protect citizens from financial exploitation (e.g., warnings that official forms are free of charge).", bold_prefix="Safety Constraints (N=150, exactly 1/task):")
    add_p(
        "Ground truth represents internal curation by the project author based on official administrative schemes, rather than an independently certified legal gold standard. The registry records scheme names and cutoff dates, but lacks direct URLs, verbatim statutory excerpts, and clause-to-fact alignment mapping. Multi-expert legal panel certification remains future work.",
        bold_prefix="Curation Scope Limitation: "
    )

    add_h2("3.3 Underlying Information Need (UIN) Formulation")
    add_p(
        "To eliminate English-normative bias—treating English sentence structure as an artificial standard of correctness—every task is indexed by an Underlying Information Need (UIN). The UIN specifies the communicative intent, necessary factual scope, conditions, and boundary caveats in language-agnostic conceptual terms. Hindi and Hinglish responses are evaluated against the UIN rather than against translated English text."
    )

    # =========================================================================
    # 4. LANGUAGE CONDITIONS AND MODEL CONFIGURATIONS
    # =========================================================================
    add_h1("4. Language Conditions and Model Configurations")
    add_h2("4.1 Language Conditions")
    add_p("Each task is operationalized across three authentic linguistic prompts:")
    add_numbered("1.", " Formal Indian English administrative query phrasing.", bold_prefix="English (ENGLISH):")
    add_numbered("2.", " Modern standard Hindi in Devanagari script, incorporating formal administrative vocabulary (yojana [scheme], patrata [eligibility], aavedan prakriya [application process]).", bold_prefix="Hindi (HINDI):")
    add_numbered("3.", " Colloquial Romanized “Hinglish” reflecting authentic mobile conversational queries (e.g., “PM-JAY card banwane ke liye eligibility kya hai aur online apply kaise karein?”).", bold_prefix="Hindi-English Code-Switching (CODE_SWITCHING):")

    add_h2("4.2 Target Model Slots & Software Configuration")
    add_p(
        "The execution protocol defines four target model slots: Google Slot (gemini-3.5-flash), OpenAI Slot (gpt-4o), Anthropic Slot (claude-3.5-sonnet), and Meta Slot (llama-3.1-70b). Prespecified generation parameters are temperature = 0.2, top_p = 1.0, and max_tokens = 1000."
    )
    add_p(
        "All four models represent architectural slots in the execution design. No live model endpoints were queried. The 5,400 records in the repository were synthesized in-memory to verify pipeline schema adherence and test automation.",
        bold_prefix="Target Slot Status: "
    )

    # =========================================================================
    # 5. DATA COLLECTION AND REPRODUCIBILITY
    # =========================================================================
    add_h1("5. Data Collection and Reproducibility")
    add_h2("5.1 Pipeline Factorial Matrix Design")
    add_p("The software pipeline verifies data collection and scoring over a full factorial matrix:")
    add_equation("Factorial Matrix = 150 Tasks × 3 Languages × 4 Model Slots × 3 Repetitions = 5,400 Factorial Cells", "1")

    # Table 2 (Execution Matrix)
    add_table_caption("Table 2: Benchmark execution matrix and synthetic pipeline fixture verification.")
    t2 = doc.add_table(rows=7, cols=5)
    t2_headers = ["Dimension", "Specification", "Levels", "Observed Fixtures", "Completeness"]
    for c_i, h in enumerate(t2_headers):
        t2.rows[0].cells[c_i].paragraphs[0].text = h
    t2_data = [
        ["Tasks", "Administrative & civic interactions", "150 tasks", "150 tasks", "100.0%"],
        ["Domains", "Healthcare, Education, Public Services, Finance, GK", "5 domains", "1,080 / domain", "100.0%"],
        ["Languages", "English, Hindi (Devanagari), Hinglish (Roman)", "3 conditions", "1,800 / condition", "100.0%"],
        ["Model Slots", "Gemini 3.5 Flash, GPT-4o, Claude 3.5 Sonnet, Llama 3.1", "4 slots", "1,350 / slot", "100.0%"],
        ["Repetitions", "Pipeline repetition slots (r = 1, 2, 3)", "3 repetitions", "1,800 / rep", "100.0%"],
        ["Total Matrix", "150 × 3 × 4 × 3 full factorial design", "5,400 cells", "5,400 fixtures", "SHA-256 Verified"]
    ]
    for r_i, row in enumerate(t2_data):
        for c_i, val in enumerate(row):
            t2.rows[r_i+1].cells[c_i].paragraphs[0].text = val
    t2_widths = [Inches(1.05), Inches(2.05), Inches(0.95), Inches(1.10), Inches(1.12)]
    t2_aligns = [WD_ALIGN_PARAGRAPH.LEFT, WD_ALIGN_PARAGRAPH.LEFT, WD_ALIGN_PARAGRAPH.CENTER, WD_ALIGN_PARAGRAPH.CENTER, WD_ALIGN_PARAGRAPH.CENTER]
    style_table(t2, t2_widths, t2_aligns)

    add_h2("5.2 Cryptographic Verification and Software Fixtures")
    add_p(
        "The dataset fixture file (stage12_4_full_evaluation_responses.json, 10,418,007 bytes) was cryptographically audited:"
    )
    add_bullet(" 095b8caa9497b4d8cf804b29baad23b4d3de813bda9f865b7a1da3ef658ca5f3", bold_prefix="Raw File Bytes SHA-256:")
    add_bullet(" 296bb1650f06cc7934f16e90ef662f9c9b0207971344b0935ee02704b8bf4248", bold_prefix="Canonical Sorted JSON SHA-256:")
    add_p("Coverage is 100.0% (5,400/5,400 unique cells; 0 missing, 0 duplicate, 0 dry-run records).")
    add_p(
        "Records were generated programmatically in 0.150 seconds by assembling task metadata, Critical Facts, and linguistic scaffolding. Recorded latency is 0 ms across all 5,400 records, and within-cell repetition variance is exactly 0.0 across all 1,800 cells. These fixtures verify that the pipeline correctly parses, validates, and serializes the complete factorial matrix.",
        bold_prefix="Baseline Fixture Characteristics: "
    )

    # =========================================================================
    # 6. METRIC DEFINITIONS AND SCORING PROTOCOL
    # =========================================================================
    add_h1("6. Metric Definitions and Scoring Protocol")
    add_p("LINGUA-AUDIT operationalizes 13 response-quality metrics categorized across five measurement dimensions (Table 3).")

    # Table 3: Metric Overview
    add_table_caption("Table 3: The 13 LINGUA-AUDIT response-quality metrics across five measurement dimensions.")
    t3 = doc.add_table(rows=14, cols=3)
    t3_headers = ["Dimension", "Metric Identifier", "Operationalized Definition"]
    for c_i, h in enumerate(t3_headers):
        t3.rows[0].cells[c_i].paragraphs[0].text = h
    t3_data = [
        ["Factual Precision", "M1: Factual Precision", "N_supported / N_adjudicated (claim-level precision)"],
        ["Factual Precision", "M1b: Contradiction-Only Precision", "N_supp / (N_supp + N_contra) (neutral assertions non-fatal)"],
        ["Completeness & Omission", "M2a: Critical Fact Coverage", "CF_covered / CF_total (CF_total = 3)"],
        ["Completeness & Omission", "M2c: Weighted Completeness", "(CF_wt + 0.5 IF_wt) / Total_wt ∈ [0, 1]"],
        ["Completeness & Omission", "M3: Critical Fact Omission Rate", "CF_omitted / CF_total (silent omission penalty)"],
        ["Factual Errors", "M4a: Deduplicated Error Count", "Contra Claims + Unlinked CF_contra"],
        ["Factual Errors", "M4b: Any Error Indicator", "Binary indicator 1(M4a > 0)"],
        ["Factual Errors", "M4c: Normalized Error Rate", "N_contra / N_adjudicated (binomial error proportion)"],
        ["Authenticity & Safety", "M5: Citation Quality Grade", "Ordinal rubric {0, 1, 2, 3, 4} (fabricated link capped at 1)"],
        ["Authenticity & Safety", "M6: Domain Safety Level", "Ordinal severity rating {0, 1, 2} (safety/fraud risk)"],
        ["Authenticity & Safety", "M7: Semantic Preservation", "Ordinal rating {0..4} anchored to language-agnostic UIN"],
        ["Stochastic Consistency", "M8a: Completeness Variance", "Sample variance s^2_CF across 3 repetitions (df = 2)"],
        ["Stochastic Consistency", "M8b: Jaccard Concordance", "|⋂ CF(ri)| / |⋃ CF(ri)| over 3 repetitions"]
    ]
    for r_i, row in enumerate(t3_data):
        for c_i, val in enumerate(row):
            t3.rows[r_i+1].cells[c_i].paragraphs[0].text = val
    t3_widths = [Inches(1.8), Inches(2.2), Inches(2.27)]
    t3_aligns = [WD_ALIGN_PARAGRAPH.LEFT, WD_ALIGN_PARAGRAPH.LEFT, WD_ALIGN_PARAGRAPH.LEFT]
    style_table(t3, t3_widths, t3_aligns)

    add_h2("6.1 Primary Confirmatory Metrics")
    add_p("• M1 — Factual Precision: Proportion of scorable extracted factual claims corroborated by statutory ground truth:")
    add_equation("M1 = N_supported / N_adjudicated = N_supported / (N_supported + N_contradicted + N_unsupported)", "2")
    add_p("If N_adjudicated = 0 (e.g., complete refusal), M1 is set to None/NA and tracked by M1,empty = 1(N_adjudicated = 0).")

    add_p("• M2a — Critical Fact Coverage: Proportion of benchmark Critical Facts covered:")
    add_equation("M2a = CF_covered / CF_total  (with CF_total = 3 for all tasks)", "3")

    add_p("• M3 — Critical Fact Omission Rate: Proportion of Critical Facts omitted:")
    add_equation("M3 = CF_omitted / CF_total", "4")
    add_p("Actively contradicted facts are tracked in M4a and separated from silent omission in M3.")

    add_h2("6.2 Secondary Metrics and Error Deduplication")
    add_p("• M4a — Deduplicated Error Count: Contradicted Critical Facts linked to an already-counted contradicted atomic claim are deduplicated to prevent artificial double-counting:")
    add_equation("M4a = |Claims_contra| + ∑ 1(unlinked(f, Claims_contra))", "5")

    add_p("• M5 — Citation Quality Grade: Evaluates portal links on a 5-point scale: Grade 0 (No citation), Grade 1 (Fabricated URL cap), Grade 2 (Irrelevant/broken link), Grade 3 (Relevant general reference), Grade 4 (Authoritative official departmental link). Any single fabricated URL strictly caps the response at Grade 1.")

    add_p("• M7 — Semantic Preservation: Ordinal rating (0 to 4) anchored to the UIN, ensuring valid vernacular phrasing and regional administrative loanwords receive full credit.")

    add_p("• M8b — Critical Fact Jaccard Concordance: Set-theoretic stability across repetitions:")
    add_equation("M8b = |CF(r1) ⋂ CF(r2) ⋂ CF(r3)| / |CF(r1) ⋃ CF(r2) ⋃ CF(r3)|", "6")

    add_h2("6.3 Software Implementation vs. Empirical Construct Validity")
    add_p(
        "All 13 metrics are implemented in backend/app/scoring/lingua_audit/metrics.py and verified by 115 passing tests. However, passing tests establish software execution correctness, numerical stability, and exception handling; they do not establish empirical construct validity. Because certified human annotation has not yet been conducted, all metrics remain strictly empirically unvalidated. The complete software implementation inventory is provided in Appendix Table A.1."
    )

    # =========================================================================
    # 7. STATISTICAL ANALYSIS PLAN
    # =========================================================================
    add_h1("7. Statistical Analysis Plan")
    add_h2("7.1 Primary Confirmatory Models (GLMMs)")
    add_p("For primary proportional outcomes bounded in [0, 1] (M1, M1b, M2a, M3, M4c), we specify Binomial GLMMs with a logit link:")
    add_equation("logit(E[Y_ijkr]) = β0 + β_lang · Lang_k + β_model · Model_m + (β_lang×model) + u_task(i) + v_family(j)", "7")
    add_p("where u_task ~ N(0, σ^2_task) and v_family ~ N(0, σ^2_family) capture random intercepts for individual tasks and scenario families.")

    add_h2("7.2 Secondary Models and Provisional Specifications")
    add_p("Secondary outcomes are modeled according to their distributional characteristics:")
    add_bullet(" Modeled via Negative Binomial GLMM with log link and an offset of log(N_adjudicated).", bold_prefix="M4a (Deduplicated Errors):")
    add_bullet(" Modeled via Cumulative Link Mixed Models (CLMM) with cumulative logit link.", bold_prefix="M5, M6, M7 (Ordinal Ratings):")
    add_bullet(" Gaussian LMM for M2c is marked provisional due to bounded support in [0, 1]; the Gamma component of the Two-Part Hurdle model for M8a is provisional because sample variances with n = 3 (df = 2) take discrete rational values; and Binomial GLMM for M8b is provisional because Jaccard denominators are random variables. Bounded fractional logit and non-parametric bootstrap will serve as comparative robustness checks.", bold_prefix="Provisional Specifications:")

    add_h2("7.3 Multiplicity Control on Confirmatory Hypothesis Family")
    add_p("To avoid diluting statistical power across 36 model-stratified subsamples, the prespecified plan designates a single primary confirmatory family: the pooled population-level language main effects across the three primary endpoints (M1, M2a, M3) across 3 pairwise contrasts (English vs. Hindi, English vs. Hinglish, Hindi vs. Hinglish):")
    add_equation("m = 3 primary endpoints × 3 pairwise language contrasts = 9 confirmatory hypotheses", "8")
    add_p(
        "Family-wise error rate across this family of 9 tests is controlled using the Holm–Bonferroni step-down procedure at an overall two-sided α = 0.05. Model-stratified contrasts (m = 36) and secondary endpoints are designated as exploratory analyses under False Discovery Rate control (FDR, q = 0.05)."
    )
    add_p("No statistical models have been fitted to data; no empirical parameters, odds ratios, or p-values have been generated.", bold_prefix="No Models Fitted to Data: ")

    # =========================================================================
    # 8. BENCHMARK AND SOFTWARE VERIFICATION RESULTS
    # =========================================================================
    add_h1("8. Benchmark and Software Verification Results")
    add_p("In accordance with strict scientific disclosure, this section reports only verified benchmark characteristics, software execution outputs, and pipeline integrity results.")

    add_h2("8.1 Benchmark Coverage and Task Characteristics")
    add_p("As summarized in Table 1, the benchmark achieves balanced coverage across all five civic domains (N = 30 tasks/domain, 450 Critical Facts, 300 Important Facts, 150 Primary Authorities). Healthcare features the highest safety sensitivity (73.3% high-risk), reflecting medical stakes, while Public Services features the highest procedural difficulty (73.3% moderate/high).")

    add_h2("8.2 Pipeline Execution Matrix Verification")
    add_p("Structural verification of the software fixture dataset across the complete factorial matrix confirms 100.0% completion across all 5,400 cells (Table 2).")

    add_h2("8.3 Synthetic Baseline Fixture Diagnostics Summary")
    add_p("Diagnostic analysis of the 5,400 synthetic software fixtures confirms expected baseline properties:")
    add_bullet(" Recorded latency is 0 ms across all 5,400 records due to in-memory template synthesis. Within-cell word length variance across the 3 repetitions is exactly 0.0 across all 1,800 cells (100.0% zero-variance).", bold_prefix="Execution Latency:")
    add_bullet(" Word counts are consistent across languages (English: 47.16 ± 6.08; Hindi: 46.16 ± 6.08; Hinglish: 46.16 ± 6.08; overall: 46.49 ± 6.10 words).", bold_prefix="Length Properties:")
    add_bullet(" English and Hinglish fixtures use 100.0% Latin characters. Hindi fixtures exhibit hybrid scaffolding (9.36% Devanagari framing characters, 90.64% Latin text for embedded factual clauses).", bold_prefix="Script Composition:")
    add_p("Detailed stratified length and script adherence tables are provided in Appendix Table B.1 and Table B.2.")

    # =========================================================================
    # 9. DISCUSSION
    # =========================================================================
    add_h1("9. Discussion: Methodological Governance and Code-Switching")
    add_h2("9.1 Auditing Substantive Information Inequality")
    add_p(
        "The central premise of LINGUA-AUDIT is that multilingual evaluations in civic domains must focus on the substantive, actionable content received by citizens rather than surface fluency. In administrative welfare schemes, subtle omissions—such as failing to mention an income cutoff or mandatory certificate attestation—have decisive consequences. LINGUA-AUDIT provides the prespecified measurement instrument to detect and quantify these disparities rigorously."
    )

    add_h2("9.2 A Cautionary Tale: Circular Evaluator Validation")
    add_p(
        "During development, an automated validation script reported near-perfect agreement (ICC = 1.0000, κ = 0.9849) between automated evaluators and purported human annotations. A provenance audit revealed these results were illusory: the script cloned evaluator output dictionaries in memory to serve as “human annotations.” By quarantining these outputs (QUARANTINE_MANIFEST.json) and explicitly disclosing that empirical evaluator validation remains pending, LINGUA-AUDIT highlights the hazard of circular self-validation in AI benchmarking."
    )

    add_h2("9.3 Authentic Code-Switching in Civic Contexts")
    add_p(
        "In South Asian digital contexts, bilingual speakers frequently employ Romanized code-switching (Hinglish) in mobile communication [13]. Evaluating models exclusively on formal English or standard Devanagari Hindi risks overlooking widespread communicative practices in multilingual communities. LINGUA-AUDIT establishes code-switching as a primary, first-class evaluation condition alongside Hindi and English."
    )

    # =========================================================================
    # 10. LIMITATIONS AND THREATS TO VALIDITY
    # =========================================================================
    add_h1("10. Limitations and Threats to Validity")
    add_numbered("1.", " Live model generations have not yet been dispatched or collected; the current 5,400-record dataset consists of deterministic programmatic fixtures. Consequently, no empirical model comparisons or language disparities can be inferred.", bold_prefix="Unexecuted Live Model Data Collection:")
    add_numbered("2.", " While a 12-item feasibility pilot package and a 270-response validation sample have been prepared, independent bilingual annotators have not yet been secured. Automated evaluators and the 13 metrics remain empirically uncalibrated against human ground truth.", bold_prefix="Pending Human Evaluator Calibration:")
    add_numbered("3.", " Tasks, Critical Facts, and Important Facts were curated internally from published schemes without direct URLs, verbatim statutory excerpts, or clause-to-fact alignment mapping. Independent multi-expert panel certification remains future work.", bold_prefix="Internal Statutory Curation Scope:")
    add_numbered("4.", " An institutional ethics protocol has been prepared (docs/ethics/ethics_application.md), but formal institutional ethics committee approval remains pending.", bold_prefix="Pending Institutional Ethics Review:")
    add_numbered("5.", " The benchmark evaluates single-turn information requests, whereas real-world civic consultations often involve multi-turn dialogues.", bold_prefix="Single-Turn Query Paradigm:")

    # =========================================================================
    # 11. ETHICS AND DATA GOVERNANCE
    # =========================================================================
    add_h1("11. Ethics and Data Governance")
    add_p(
        "The benchmark queries public administrative statutes and civic welfare schemes. No private personal data or health records were collected. An institutional ethics protocol specifies fair compensation standards for bilingual annotators; formal ethics committee approval is pending review, and no human annotators were recruited prior to approval."
    )
    add_p(
        "All benchmark tasks, ground-truth references, and scoring implementations are prepared for release under open research licenses (intended CC-BY-NC 4.0) upon final publication, though a formal standalone LICENSE file has not yet been committed to the repository root."
    )

    # =========================================================================
    # 12. CONCLUSION AND FUTURE WORK
    # =========================================================================
    add_h1("12. Conclusion and Future Work")
    add_p(
        "LINGUA-AUDIT establishes an open, reproducible framework designed to test for information inequality in multilingual AI systems. By grounding 150 civic tasks in statutory documentation across five essential domains, formalizing 13 multi-dimensional response-quality metrics, formulating a prespecified statistical analysis plan, and verifying a full factorial software pipeline across 5,400 cells, the framework provides the proposed methodological and computational infrastructure to audit whether frontier language models introduce disparities across languages."
    )
    add_p("Immediate next steps span two distinct operational tracks followed by downstream analysis:")
    add_numbered("1.", " Executing and archiving genuine model responses from external provider APIs across the 5,400 factorial matrix cells.", bold_prefix="Data Collection Track (Live API Execution):")
    add_numbered("2.", " Securing institutional ethics review approval, recruiting certified bilingual annotators, and executing the 12-item pilot and 270-response validation sample to compute genuine inter-rater reliability and calibrate automated evaluators.", bold_prefix="Evaluator Calibration Track (Human Ground Truth):")
    add_numbered("3.", " Applying the calibrated evaluation pipeline to genuine model responses and fitting the prespecified GLMMs to test for multilingual information inequality.", bold_prefix="Downstream Empirical Scoring and Estimation:")

    # Reproducibility Statement
    add_h2("Reproducibility Statement")
    add_p("All research materials are preserved within the repository:")
    add_bullet(" data/benchmark/master_task_registry_150.json (SHA-256: 2ce2cb688c011cb0279425a3c063ce4e5b7b6a2354a4aa9df75a77efa9d00315).", bold_prefix="Benchmark Registry:")
    add_bullet(" data/benchmark/raw_responses/stage12_4_full_evaluation_responses.json (Raw bytes SHA-256: 095b8caa...; Canonical sorted JSON SHA-256: 296bb165...).", bold_prefix="Pipeline Fixture Dataset:")
    add_bullet(" Modular Python package in backend/app/scoring/lingua_audit/, accompanied by 115 passing tests (pytest tests/).", bold_prefix="Scoring Implementation:")
    add_bullet(" Blinded 12-item packages stage12_5_2D_pilot_annotator_A.json and B.json, along with restricted key stage12_5_2D_pilot_restricted_mapping.json.", bold_prefix="Feasibility Pilot Packages:")
    add_bullet(" Documented invalid synthetic artifacts in data/benchmark/evaluator_validation/QUARANTINE_MANIFEST.json.", bold_prefix="Quarantine Manifest:")
    add_bullet(" scratch/reproduce_paper_analysis.py reproduces all reported summary outputs in paper/results/.", bold_prefix="Reproduction Script:")

    # =========================================================================
    # REFERENCES (NEW PAGE, IEEE STYLE)
    # =========================================================================
    doc.add_page_break()
    add_h1("References")
    
    references = [
        "[1] D. Hendrycks, C. Burns, S. Basart, A. Zou, M. Mazeika, D. Song, and J. Steinhardt, “Measuring massive multitask language understanding,” in Proc. Int. Conf. Learn. Representations (ICLR), 2021.",
        "[2] A. Conneau, R. Rinott, G. Lample, A. Williams, S. Bowman, H. Schwenk, and V. Stoyanov, “XNLI: Evaluating cross-lingual sentence representations,” in Proc. Conf. Empirical Methods Natural Lang. Process. (EMNLP), 2018, pp. 2475–2485.",
        "[3] D. Blasi, A. Antonovsky, A. Anastasopoulos, G. Neubig, and R. Cotterell, “Systematic inequalities in language technology performance across the world's languages,” in Proc. 60th Annu. Meeting Assoc. Comput. Linguistics (ACL), 2022, pp. 5486–5505.",
        "[4] P. Joshi, S. Santy, A. Budhiraja, K. Bali, and M. Choudhury, “The state and fate of linguistic diversity and inclusion in the NLP world,” in Proc. 58th Annu. Meeting Assoc. Comput. Linguistics (ACL), 2020, pp. 6282–6293.",
        "[5] E. M. Bender, T. Gebru, A. McMillan-Major, and S. Shmitchell, “On the dangers of stochastic parrots: Can language models be too big?,” in Proc. ACM Conf. Fairness Accountability Transparency (FAccT), 2021, pp. 610–623.",
        "[6] J. H. Clark, E. Choi, M. Collins, D. Garrette, T. Kwiatkowski, V. Nikolaev, and J. Palomaki, “TyDi QA: A benchmark for information-seeking QA in typologically diverse languages,” Trans. Assoc. Comput. Linguistics (TACL), vol. 8, pp. 454–470, 2020.",
        "[7] K. Ahuja, H. Diddee, R. Hada, M. Ochieng, K. Ramesh, P. Jain, A. Nambi, T. Ganu, S. Segal, M. Ahmed, K. Bali, and S. Sitaram, “MEGA: Multilingual evaluation of generative AI,” in Proc. Conf. Empirical Methods Natural Lang. Process. (EMNLP), 2023, pp. 4232–4267.",
        "[8] Y. Bang, S. Cahyawijaya, N. Lee, W. Dai, D. Su, B. Wilie, H. Lovenia, Z. Ji, T. Yu, W. Chung, Q. V. Do, Y. Xu, and P. Fung, “A multitask, multilingual, multimodal evaluation of ChatGPT on reasoning, hallucination, and interactivity,” in Proc. 13th Int. Joint Conf. Natural Lang. Process. 3rd Conf. Asia-Pacific Chapter Assoc. Comput. Linguistics (IJCNLP-AACL), 2023, pp. 675–718.",
        "[9] H. Singh, N. Gupta, S. Bharadwaj, D. Tewari, and P. Talukdar, “IndicGenBench: A multilingual benchmark to evaluate generation capabilities of LLMs on Indic languages,” in Findings Assoc. Comput. Linguistics: ACL 2024, 2024, pp. 10041–10061.",
        "[10] A. K. Singh, V. Kumar, R. Murthy, J. Sen, A. Mittal, and G. Ramakrishnan, “INDIC QA BENCHMARK: A multilingual benchmark to evaluate question answering capability of LLMs for Indic languages,” in Findings Assoc. Comput. Linguistics: EMNLP 2024, 2024, pp. 16231–16248.",
        "[11] OpenAI, “IndQA: Evaluating cultural fluency and context in Indian languages,” OpenAI Research, Tech. Rep., 2025.",
        "[12] N. Majithia, R. Shinde, Z. Chapman, P. Trital, J. Decker, M. Maskey, E. Simperl, and N. Shadbolt, “The CitizenQuery benchmark: A novel dataset and evaluation pipeline for measuring LLM performance in citizen query tasks,” arXiv preprint arXiv:2602.04064, 2026.",
        "[13] S. Khanuja, S. Dandapat, A. Srinivasan, S. Sitaram, and M. Choudhury, “GLUECoS: An evaluation benchmark for code-switched NLP,” in Proc. 58th Annu. Meeting Assoc. Comput. Linguistics (ACL), 2020, pp. 3575–3585.",
        "[14] S. Min, K. Krishna, X. Lyu, M. Lewis, W. Yih, P. W. Koh, M. Iyyer, L. Zettlemoyer, and H. Hajishirzi, “FActScore: Fine-grained atomic evaluation of factual precision in long form text generation,” in Proc. Conf. Empirical Methods Natural Lang. Process. (EMNLP), 2023, pp. 12076–12099.",
        "[15] P. Liang, R. Bommasani, T. Lee, D. Tsipras, D. Soylu, M. Yasunaga, Y. Zhang, D. Narayanan, Y. Wu, A. Kumar, B. Newman, et al., “Holistic evaluation of language models,” Trans. Mach. Learn. Res. (TMLR), pp. 2835–8856, 2023.",
        "[16] L. Zheng, W. L. Chiang, Y. Sheng, S. Zhuang, Z. Wu, Y. Zhuang, Z. Lin, Z. Li, D. Li, E. Xing, H. Zhang, J. E. Gonzalez, and I. Stoica, “Judging LLM-as-a-judge with MT-Bench and Chatbot Arena,” in Adv. Neural Inf. Process. Syst. (NeurIPS), vol. 36, 2023, pp. 46595–46623.",
        "[17] R. Hada, V. Gumma, A. de Wynter, H. Diddee, M. Ahmed, M. Choudhury, K. Bali, and S. Sitaram, “Are large language model-based evaluators the solution to scaling up multilingual evaluation?,” arXiv preprint arXiv:2309.07462, 2023."
    ]
    for ref in references:
        p_ref = doc.add_paragraph()
        p_ref.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        p_ref.paragraph_format.left_indent = Inches(0.35)
        p_ref.paragraph_format.first_line_indent = Inches(-0.35)
        p_ref.paragraph_format.space_before = Pt(2)
        p_ref.paragraph_format.space_after = Pt(4)
        p_ref.paragraph_format.line_spacing = 1.05
        r = p_ref.add_run(ref)
        r.font.name = "Times New Roman"
        r.font.size = Pt(9.5)

    # =========================================================================
    # APPENDIX A (NEW PAGE)
    # =========================================================================
    doc.add_page_break()
    p_aph = add_h1("Appendix A: Metric Inventory & Verification Status")
    p_aph.paragraph_format.space_before = Pt(6)
    p_aph.paragraph_format.space_after = Pt(3)
    p_ap_intro = add_p(
        "Table A.1 documents the complete operational specification, target statistical model, and software verification status for all 13 response-quality metrics. Implementation in the Python scoring package (backend/app/scoring/lingua_audit/metrics.py) and 115 passing tests confirm algorithmic execution correctness, not empirical construct validity. All metrics remain empirically unvalidated pending future human annotation.",
        space_after=3
    )

    add_table_caption("Table A.1: Complete LINGUA-AUDIT metric implementation inventory and software verification status.")
    
    # 5 generous columns (Total width = 6.27 inches):
    # 1. Metric Code: 0.58 in
    # 2. Metric Name: 1.30 in
    # 3. Operationalized Formula / Rubric: 1.55 in
    # 4. Prespecified Role: 1.10 in
    # 5. Target Statistical Model & Verification Status: 1.74 in
    ta1 = doc.add_table(rows=14, cols=5)
    ta1_headers = [
        "Code", 
        "Metric Name", 
        "Operationalized Formula / Rubric", 
        "Prespecified Role", 
        "Target Model & Verification Status"
    ]
    for c_i, h in enumerate(ta1_headers):
        ta1.rows[0].cells[c_i].paragraphs[0].text = h
    ta1_data = [
        ["M1", "Factual Precision", "N_Supp / N_adjudicated", "Primary Confirmatory", "Binomial GLMM (logit link) • Code & 115 Tests: Verified • Validation: UNVALIDATED*"],
        ["M1b", "Contradiction Precision", "N_Supp / (N_Supp + N_Contra)", "Secondary Sensitivity", "Binomial GLMM (logit link) • Code & 115 Tests: Verified • Validation: UNVALIDATED*"],
        ["M2a", "Critical Fact Coverage", "CF_covered / CF_total", "Primary Confirmatory", "Binomial GLMM (logit link) • Code & 115 Tests: Verified • Validation: UNVALIDATED*"],
        ["M2c", "Weighted Completeness", "(sum CF_wt + 0.5 sum IF_wt) / Total_wt", "Secondary Sensitivity", "Linear Mixed Model (LMM) [Provisional; Bounded] • Code & Tests: Verified • Validation: UNVALIDATED*"],
        ["M3", "Critical Fact Omission", "CF_omitted / CF_total", "Primary Confirmatory", "Binomial GLMM (logit link) • Code & 115 Tests: Verified • Validation: UNVALIDATED*"],
        ["M4a", "Deduplicated Error Count", "card(Claims_contra) + sum unlinked(CF_contra)", "Secondary Confirmatory", "Negative Binomial GLMM (log link, log offset) • Code & Tests: Verified • Validation: UNVALIDATED*"],
        ["M4b", "Any Error Indicator", "1(M4a > 0)", "Secondary Confirmatory", "Binomial GLMM (logit link) • Code & 115 Tests: Verified • Validation: UNVALIDATED*"],
        ["M4c", "Normalized Error Rate", "N_Contra / N_adjudicated", "Secondary Confirmatory", "Binomial GLMM (logit link) • Code & 115 Tests: Verified • Validation: UNVALIDATED*"],
        ["M5", "Citation Quality Grade", "Ordinal rubric {0, 1, 2, 3, 4}", "Secondary Confirmatory", "Cumulative Link Mixed Model (CLMM) • Code & Tests: Verified • Validation: UNVALIDATED*"],
        ["M6", "Domain Safety Level", "Ordinal scale {0, 1, 2}", "Secondary Confirmatory", "Cumulative Link Mixed Model (CLMM) • Code & Tests: Verified • Validation: UNVALIDATED*"],
        ["M7", "Semantic Preservation", "Ordinal scale {0..4} (anchored to UIN)", "Secondary Confirmatory", "Cumulative Link Mixed Model (CLMM) • Code & Tests: Verified • Validation: UNVALIDATED*"],
        ["M8a", "Completeness Variance", "s^2_CF across 3 repetitions", "Secondary Confirmatory", "Two-Part Hurdle GLMM (Logit + Gamma) [Provisional] • Code & Tests: Verified • Validation: UNVALIDATED*"],
        ["M8b", "Jaccard Concordance", "K_overlap / K_union across 3 reps", "Secondary Confirmatory", "Binomial GLMM (logit link) [Provisional] • Code & Tests: Verified • Validation: UNVALIDATED*"]
    ]
    for r_i, row in enumerate(ta1_data):
        for c_i, val in enumerate(row):
            ta1.rows[r_i+1].cells[c_i].paragraphs[0].text = val
    ta1_widths = [Inches(0.58), Inches(1.30), Inches(1.55), Inches(1.10), Inches(1.74)]
    ta1_aligns = [WD_ALIGN_PARAGRAPH.LEFT, WD_ALIGN_PARAGRAPH.LEFT, WD_ALIGN_PARAGRAPH.LEFT, WD_ALIGN_PARAGRAPH.LEFT, WD_ALIGN_PARAGRAPH.LEFT]
    style_table(ta1, ta1_widths, ta1_aligns, font_size_pt=8.0, cell_pad_v=25)

    p_note_a1 = doc.add_paragraph()
    p_note_a1.paragraph_format.space_before = Pt(2)
    p_note_a1.paragraph_format.space_after = Pt(4)
    r_na = p_note_a1.add_run("*Validation Status Note: All 13 metrics are fully implemented and verified against unit and regression tests (115 passing tests), but remain strictly empirically unvalidated pending future bilingual human annotation.")
    r_na.font.name = "Times New Roman"
    r_na.font.size = Pt(8.0)
    r_na.italic = True
    r_na.font.color.rgb = RGBColor(71, 85, 105)

    # =========================================================================
    # APPENDIX B (NEW PAGE)
    # =========================================================================
    doc.add_page_break()
    p_bph = add_h1("Appendix B: Synthetic Baseline Fixture Diagnostics")
    p_bph.paragraph_format.space_before = Pt(6)
    p_bph.paragraph_format.space_after = Pt(3)
    add_p(
        "Table B.1 and Table B.2 report the detailed stratified text and script adherence metrics computed from the 5,400 programmatic software verification fixtures.",
        space_after=3
    )

    add_table_caption("Table B.1: Synthetic fixture diagnostic characteristics across language scaffolding.")
    tb1 = doc.add_table(rows=10, cols=7)
    tb1_headers = [
        "Condition / Stratum", 
        "N", 
        "Char Length (Mean ± SD)", 
        "Char Length (Median [IQR])", 
        "Word Count (Mean ± SD)", 
        "Word Count (Median [IQR])", 
        "Latency"
    ]
    for c_i, h in enumerate(tb1_headers):
        tb1.rows[0].cells[c_i].paragraphs[0].text = h
    tb1_data = [
        ["Language: English", "1,800", "339.80 ± 45.33", "340.0 [57.0]", "47.16 ± 6.08", "47.0 [7.0]", "0 ms*"],
        ["Language: Hindi", "1,800", "326.80 ± 45.33", "327.0 [57.0]", "46.16 ± 6.08", "46.0 [7.0]", "0 ms*"],
        ["Language: Hinglish", "1,800", "333.80 ± 45.33", "334.0 [57.0]", "46.16 ± 6.08", "46.0 [7.0]", "0 ms*"],
        ["Model Slot: Gemini 3.5 Flash", "1,350", "333.47 ± 45.64", "337.0 [65.0]", "46.49 ± 6.10", "46.0 [7.0]", "0 ms*"],
        ["Model Slot: GPT-4o", "1,350", "333.47 ± 45.64", "337.0 [65.0]", "46.49 ± 6.10", "46.0 [7.0]", "0 ms*"],
        ["Model Slot: Claude 3.5 Sonnet", "1,350", "333.47 ± 45.64", "337.0 [65.0]", "46.49 ± 6.10", "46.0 [7.0]", "0 ms*"],
        ["Model Slot: Llama 3.1 70B", "1,350", "333.47 ± 45.64", "337.0 [65.0]", "46.49 ± 6.10", "46.0 [7.0]", "0 ms*"],
        ["Fixture Total", "5,400", "333.47 ± 45.64", "337.0 [65.0]", "46.49 ± 6.10", "46.0 [7.0]", "0 ms*"],
        ["*Recorded latency is 0 ms across all 5,400 records due to in-memory template synthesis. Within-cell word length variance across repetitions is exactly 0.0.", "", "", "", "", "", ""]
    ]
    for r_i, row in enumerate(tb1_data):
        for c_i, val in enumerate(row):
            tb1.rows[r_i+1].cells[c_i].paragraphs[0].text = val
    tb1_widths = [Inches(1.25), Inches(0.42), Inches(1.05), Inches(1.05), Inches(0.95), Inches(0.95), Inches(0.60)]
    tb1_aligns = [WD_ALIGN_PARAGRAPH.LEFT, WD_ALIGN_PARAGRAPH.CENTER, WD_ALIGN_PARAGRAPH.CENTER, WD_ALIGN_PARAGRAPH.CENTER, WD_ALIGN_PARAGRAPH.CENTER, WD_ALIGN_PARAGRAPH.CENTER, WD_ALIGN_PARAGRAPH.CENTER]
    style_table(tb1, tb1_widths, tb1_aligns, font_size_pt=8.5)

    add_table_caption("Table B.2: Synthetic fixture script composition across language conditions.")
    tb2 = doc.add_table(rows=5, cols=8)
    tb2_headers = [
        "Language Condition", 
        "Fixtures", 
        "Devanagari Chars", 
        "Latin Chars", 
        "Punctuation", 
        "Devanagari %", 
        "Latin %", 
        "Script Profile Interpretation"
    ]
    for c_i, h in enumerate(tb2_headers):
        tb2.rows[0].cells[c_i].paragraphs[0].text = h
    tb2_data = [
        ["English", "1,800", "0", "467,280", "144,360", "0.0%", "100.0%", "Pure Latin typography"],
        ["Hindi", "1,800", "41,400", "400,680", "146,160", "9.36%", "90.64%", "Hybrid framing (Devanagari scaffolding)"],
        ["Hinglish", "1,800", "0", "458,280", "142,560", "0.0%", "100.0%", "Romanized code-switching"],
        ["Total", "5,400", "41,400", "1,326,240", "433,080", "—", "—", "Full Synthetic Fixture Corpus"]
    ]
    for r_i, row in enumerate(tb2_data):
        for c_i, val in enumerate(row):
            tb2.rows[r_i+1].cells[c_i].paragraphs[0].text = val
    tb2_widths = [Inches(1.00), Inches(0.55), Inches(0.75), Inches(0.75), Inches(0.75), Inches(0.70), Inches(0.65), Inches(1.12)]
    tb2_aligns = [WD_ALIGN_PARAGRAPH.LEFT, WD_ALIGN_PARAGRAPH.CENTER, WD_ALIGN_PARAGRAPH.CENTER, WD_ALIGN_PARAGRAPH.CENTER, WD_ALIGN_PARAGRAPH.CENTER, WD_ALIGN_PARAGRAPH.CENTER, WD_ALIGN_PARAGRAPH.CENTER, WD_ALIGN_PARAGRAPH.LEFT]
    style_table(tb2, tb2_widths, tb2_aligns, font_size_pt=8.5)

    out_dir = "paper/final"
    os.makedirs(out_dir, exist_ok=True)
    out_file = os.path.join(out_dir, "LINGUA_AUDIT_final.docx")
    doc.save(out_file)
    print(f"Successfully generated: {out_file}")

if __name__ == "__main__":
    create_document()
