import os
import json
import fitz
import argparse
from datetime import datetime
import re

def extract_sections_and_subsections(pdf_path):
    doc = fitz.open(pdf_path)
    section_texts = []

    all_spans = []
    for page_num, page in enumerate(doc):
        blocks = page.get_text("dict")["blocks"]
        for block in blocks:
            if block.get("type") != 0:
                continue
            for line in block["lines"]:
                for span in line["spans"]:
                    text = span["text"].strip()
                    if not text:
                        continue
                    all_spans.append({
                        "text": text,
                        "size": span["size"],
                        "flags": span["flags"],
                        "page": page_num + 1,
                        "y": span["bbox"][1]
                    })

    sizes = [s["size"] for s in all_spans]
    max_size = max(sizes) if sizes else 12
    h1 = max_size * 0.9
    h2 = max_size * 0.75

    headings = []
    for idx, span in enumerate(all_spans):
        text = span["text"]
        level = None
        if span["size"] >= h1:
            level = "H1"
        elif span["size"] >= h2:
            level = "H2"
        elif span["flags"] & 16:
            level = "H2"
        if level:
            headings.append((idx, text, span["page"]))

    for i, (start_idx, title, page) in enumerate(headings):
        end_idx = headings[i + 1][0] if i + 1 < len(headings) else len(all_spans)
        body = " ".join([s["text"] for s in all_spans[start_idx:end_idx]])
        cleaned = re.sub(r"\s+", " ", body.strip())
        section_texts.append({
            "section_title": title,
            "refined_text": cleaned,
            "page_number": page
        })

    doc.close()
    return section_texts

def task2_process(pdf_dir, output_file, persona, job):
    keywords = set(re.findall(r'\w+', persona.lower() + " " + job.lower()))

    results = []
    input_docs = []
    for root, _, files in os.walk(pdf_dir):
        for file in files:
            if file.lower().endswith('.pdf'):
                path = os.path.join(root, file)
                input_docs.append(file)
                sections = extract_sections_and_subsections(path)
                for sec in sections:
                    score = sum(word in sec["refined_text"].lower() for word in keywords)
                    results.append({
                        "document": file,
                        **sec,
                        "score": score
                    })

    results = sorted(results, key=lambda x: -x["score"])[:10]

    extracted_sections = []
    subsection_analysis = []
    for i, res in enumerate(results, 1):
        extracted_sections.append({
            "document": res["document"],
            "section_title": res["section_title"],
            "page_number": res["page_number"],
            "importance_rank": i
        })
        subsection_analysis.append({
            "document": res["document"],
            "refined_text": res["refined_text"],
            "page_number": res["page_number"]
        })

    final = {
        "metadata": {
            "input_documents": list(set(input_docs)),
            "persona": persona,
            "job_to_be_done": job,
            "processing_timestamp": str(datetime.now())
        },
        "extracted_sections": extracted_sections,
        "subsection_analysis": subsection_analysis
    }

    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(final, f, indent=2, ensure_ascii=False)

    print(f"✅ DONE. Output written to {output_file}")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True)
    parser.add_argument("--output", required=True)
    parser.add_argument("--persona", required=True)
    parser.add_argument("--job", required=True)
    args = parser.parse_args()

    task2_process(args.input, args.output, args.persona, args.job)

if __name__ == "__main__":
    main()
