# Adobe Hackathon 2025 – Approach Explanation (Task 1a & 1b)

## Task 1a – PDF Outline Extraction

The solution uses the PyMuPDF library to parse each PDF page, extract spans, and detect headings using font size, font name, and bold flags. Headings are then classified into "H1", "H2", and "H3" based on relative size thresholds (e.g., top 5%, bold/large font).

Outlines are sorted using `(page_number, y_position)` to maintain reading order. A fallback is used to extract the document title from the first large/bold text on the first page if no metadata title is found. The script supports multilingual PDFs and is designed to work across diverse layouts (technical, business, textbooks).

## Task 1b – Persona-Driven Section Extraction

This script extends Task 1a and supports collection inputs (3–10 PDFs). It takes dynamic inputs: `--input`, `--persona`, and `--job`, and processes the entire folder as a document collection.

Text spans are grouped into sections using heading detection logic (bold/large fonts or numbered formats). Each section is extracted with surrounding text as `refined_text`.

Relevance is computed by matching keywords from the persona and job to both section titles and refined text. Scores are summed and top N sections are selected. This supports ranking sections for multiple-persona use cases. Each output JSON includes:
- metadata
- extracted_sections
- subsection_analysis

## Docker + Constraints

All code executes in a CPU-only environment with PyMuPDF (tiny, <50MB). No internet or API calls are used. Each script runs in <60 seconds for typical docs, and Docker volume maps /app/input and /app/output, running securely offline.

