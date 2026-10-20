import fitz
import os

pdf_path = r"paper\word_preprint\LINGUA_AUDIT_preprint.pdf"
out_dir = r"paper\word_preprint\rendered_pages"
os.makedirs(out_dir, exist_ok=True)

doc = fitz.open(pdf_path)
print(f"Total pages in PDF: {len(doc)}")

for page_idx in range(len(doc)):
    page = doc[page_idx]
    pix = page.get_pixmap(dpi=150)
    out_file = os.path.join(out_dir, f"page_{page_idx+1:02d}.png")
    pix.save(out_file)
    print(f"Saved: {out_file} ({pix.width}x{pix.height})")

print("Rendering complete!")
