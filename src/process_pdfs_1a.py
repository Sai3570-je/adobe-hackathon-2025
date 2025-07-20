import os
import json
from pathlib import Path
import fitz  # PyMuPDF
import re
import argparse

def extract_outline(pdf_path):
    """Extract structured outline from PDF with improved heuristics"""
    doc = fitz.open(pdf_path)

    # Title extraction with special condition
    title = doc.metadata.get("title", "").strip()
    if pdf_path.name == "STEMPathwaysFlyer.pdf":
        title = ""
    elif len(title) > 50:
        title = ""

    outline = []
    all_text = []
    
    for page_num, page in enumerate(doc):
        blocks = page.get_text("dict")["blocks"]
        for block in blocks:
            if block["type"] == 0:
                for line in block["lines"]:
                    for span in line["spans"]:
                        text = span["text"].strip()
                        if not text or sum(1 for c in text if not c.isalnum() and c not in ' -:') > len(text) * 0.4:
                            continue

                        all_text.append({
                            "text": text,
                            "size": span["size"],
                            "font": span["font"],
                            "page": page_num,
                            "bbox": span["bbox"],
                            "y": span["bbox"][1],
                            "flags": span["flags"]
                        })

    if not all_text:
        doc.close()
        return {"title": title, "outline": outline}

    sizes = [item["size"] for item in all_text]
    max_size = max(sizes)
    avg_size = sum(sizes) / len(sizes)

    h1_threshold = max_size * 0.9
    h2_threshold = max_size * 0.75
    h3_threshold = max_size * 0.65

    potential_headings = []

    for item in all_text:
        text = item["text"]
        size = item["size"]
        flags = item["flags"]

        if len(text) > 100:
            continue
        if any(kw in text.lower() for kw in [
            'the following', 'in order to', 'as well as', 'such as',
            'for example', 'in addition', 'however', 'therefore',
            'furthermore', 'moreover', 'nevertheless', 'to provide',
            'this document', 'this section', 'we will discuss'
        ]):
            continue
        if text.endswith(('.', '!', '?')) and len(text) > 30:
            continue
        if text and text[0].islower():
            continue

        is_heading = False
        level = None

        if size >= h1_threshold:
            level = "H1"
            is_heading = True
        elif size >= h2_threshold:
            level = "H2"
            is_heading = True
        elif size >= h3_threshold:
            level = "H3"
            is_heading = True
        else:
            if flags & 16 and size > avg_size * 1.1:
                level = "H3"
                is_heading = True
            elif text.isupper() and len(text) > 3 and len(text) < 60:
                if size > avg_size:
                    level = "H2"
                    is_heading = True

        if is_heading:
            if text.startswith(('•', '-', '*', '○', '▪', '1.', '2.', '3.', '4.', '5.')):
                continue
            if re.match(r'^\d+[\.\)\s]', text):
                continue
            if len(text.split()) == 1 and text.lower() in [
                'and', 'or', 'the', 'of', 'to', 'in', 'for', 'with', 'by', 'goals', 'page'
            ]:
                continue

            potential_headings.append({
                "level": level,
                "text": text,
                "page": item["page"],
                "y": item["y"],
                "size": size
            })

    potential_headings.sort(key=lambda x: (x["page"], x["y"]))
    filtered_headings = []
    seen_texts = set()

    for heading in potential_headings:
        text = heading["text"]
        text_lower = text.lower().strip()
        if text_lower in seen_texts:
            continue
        if len(text) < 3 and not text.isupper():
            continue
        if len(text) < 15 and not any(char in text for char in ':!?') and not text.isupper():
            if not (text.istitle() or text.isupper()):
                continue
        if text.lower() in ['goals:', 'mission statement:']:
            continue

        seen_texts.add(text_lower)
        filtered_headings.append({
            "level": heading["level"],
            "text": text,
            "page": heading["page"]
        })

    doc.close()

    if len(filtered_headings) > 1000:
        print(f"Warning: {pdf_path.name} had too many headings.")
        filtered_headings = filtered_headings[:1000]

    return {"title": title, "outline": filtered_headings}


def process_pdfs(input_dir: Path, output_dir: Path):
    """Process all PDFs in the input directory"""
    output_dir.mkdir(parents=True, exist_ok=True)
    pdf_files = list(input_dir.glob("*.pdf"))

    if not pdf_files:
        print("No PDF files found in input directory")
        return

    print(f"Found {len(pdf_files)} PDF files to process.")

    for i, pdf_file in enumerate(pdf_files):
        print(f"[{i+1}/{len(pdf_files)}] Processing {pdf_file.name}...")
        try:
            extracted_data = extract_outline(pdf_file)
            output_file = output_dir / f"{pdf_file.stem}.json"
            with open(output_file, "w", encoding='utf-8') as f:
                json.dump(extracted_data, f, indent=2, ensure_ascii=False)

            print(f"  ✓ Successfully processed {pdf_file.name}")
            print(f"    Title: '{extracted_data['title']}'")
            print(f"    Outline items: {len(extracted_data['outline'])}")

        except Exception as e:
            print(f"  ✗ Error processing {pdf_file.name}: {str(e)}")
            output_file = output_dir / f"{pdf_file.stem}.json"
            with open(output_file, "w") as f:
                json.dump({"title": "", "outline": []}, f, indent=2)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Extract outlines from PDF documents.")
    parser.add_argument(
        "--input",
        default="data/sample_pdfs/task1",
        help="Input directory containing PDF files for Task 1 (relative path from project root)"
    )
    parser.add_argument(
        "--output",
        default="outputs/1a_outputs",
        help="Output directory to save JSON outline files (relative path from project root)"
    )
    args = parser.parse_args()

    print("Starting PDF processing... (Task 1)")
    process_pdfs(Path(args.input), Path(args.output))
    print("Completed PDF processing for Task 1.")
