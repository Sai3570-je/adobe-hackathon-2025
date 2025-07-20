# Adobe India Hackathon 2025 – PDF Processing Solutions

This repository contains complete, efficient solutions for:

- **Task 1a:** PDF outline extraction
- **Task 1b:** Advanced PDF section/subsection extraction with persona-driven ranking

There is **no separate Task 2**—all collection/persona outputs are handled via Task 1b as per the official instructions.

## 📁 Directory Structure

```text
submission/
│
├── src/
│   ├── process_pdfs_1a.py         # Task 1a: PDF outline extraction
│   ├── process_pdfs_1b.py         # Task 1b: Section extraction, ranking, persona analysis (collections)
│   └── requirements.txt           # PyMuPDF dependency
│
├── data/
│   └── sample_pdfs/
│       ├── task1/                     # PDFs for Task 1a
│       └── task2/
│           ├── Collection 1/PDFs/     # PDFs for Collection 1
│           ├── Collection 2/PDFs/     # PDFs for Collection 2
│           └── Collection 3/PDFs/     # PDFs for Collection 3
│
├── outputs/
│   ├── 1a_outputs/                # Task 1a JSONs (per PDF)
│   └── 1b_outputs/
│       ├── Collection1/           # Task 1b JSONs (per PDF, persona-aware)
│       ├── Collection2/
│       └── Collection3/
│
├── Dockerfile
└── README.md (this file)
```

## 🖥️ Dependencies

Install dependencies (from project root):

```sh
pip install -r src/requirements.txt
```

`src/requirements.txt` contents:
```
PyMuPDF==1.22.3
```

- Scripts run CPU-only, offline, <60s per collection, model size <1GB.

## 🚩 Task 1a — PDF Outline Extraction

**Extracts document title and clean hierarchical outline for each PDF.**

### **Run Locally:**

```sh
python src/process_pdfs_1a.py --input data/sample_pdfs/task1 --output outputs/1a_outputs
```

- **Input:** All PDFs in `data/sample_pdfs/task1`
- **Output:** One JSON per PDF in `outputs/1a_outputs/`

### **Run with Docker (PowerShell-ready):**

```powershell
docker run --rm `
  -v "C:/Users/saiph/Downloads/final_submission/submission/data/sample_pdfs/task1:/app/input" `
  -v "C:/Users/saiph/Downloads/final_submission/submission/outputs/1a_outputs:/app/output" `
  --network none `
  adobehackathon2025 `
  python process_pdfs_1a.py --input /app/input --output /app/output
```

## 🚩 Task 1b — Advanced Section Extraction (and Persona-Driven Collections)

**Extracts, ranks sections/subsections, and supports persona-driven analysis over document collections (e.g., Collection 1/2/3).**

### **Run ONE Collection at a Time (Local, for each):**

(*Always run from the `submission` folder!*)

#### Collection 1:
```sh
python src/process_pdfs_1b.py --input "data/sample_pdfs/task2/Collection 1/PDFs" --output "outputs/1b_outputs/Collection1" --persona "Travel Planner" --job "Plan a trip of 4 days for a group of 10 college friends."
```
#### Collection 2:
```sh
python src/process_pdfs_1b.py --input "data/sample_pdfs/task2/Collection 2/PDFs" --output "outputs/1b_outputs/Collection2" --persona "Investment Analyst" --job "Analyze revenue trends, R&D investments, and market positioning strategies"
```
#### Collection 3:
```sh
python src/process_pdfs_1b.py --input "data/sample_pdfs/task2/Collection 3/PDFs" --output "outputs/1b_outputs/Collection3" --persona "Undergraduate Chemistry Student" --job "Identify key concepts and mechanisms for exam preparation on reaction kinetics"
```

- **Each run processes all PDFs in the collection input folder, and writes** one JSON per PDF **to the output folder.**

### **Run with Docker (PowerShell-ready):**

#### Collection 1:
```powershell
docker run --rm `
  -v "C:/Users/saiph/Downloads/final_submission/submission/data/sample_pdfs/task2/Collection 1/PDFs:/app/input" `
  -v "C:/Users/saiph/Downloads/final_submission/submission/outputs/1b_outputs/Collection1:/app/output" `
  --network none `
  adobehackathon2025 `
  python process_pdfs_1b.py --input /app/input --output /app/output --persona "Travel Planner" --job "Plan a trip of 4 days for a group of 10 college friends."
```
#### Collection 2:
```powershell
docker run --rm `
  -v "C:/Users/saiph/Downloads/final_submission/submission/data/sample_pdfs/task2/Collection 2/PDFs:/app/input" `
  -v "C:/Users/saiph/Downloads/final_submission/submission/outputs/1b_outputs/Collection2:/app/output" `
  --network none `
  adobehackathon2025 `
  python process_pdfs_1b.py --input /app/input --output /app/output --persona "Investment Analyst" --job "Analyze revenue trends, R&D investments, and market positioning strategies"
```
#### Collection 3:
```powershell
docker run --rm `
  -v "C:/Users/saiph/Downloads/final_submission/submission/data/sample_pdfs/task2/Collection 3/PDFs:/app/input" `
  -v "C:/Users/saiph/Downloads/final_submission/submission/outputs/1b_outputs/Collection3:/app/output" `
  --network none `
  adobehackathon2025 `
  python process_pdfs_1b.py --input /app/input --output /app/output --persona "Undergraduate Chemistry Student" --job "Identify key concepts and mechanisms for exam preparation on reaction kinetics"
```

## ✅ Output Format

- **Task 1a:**  
  Each JSON includes `"title"` and `"outline"`.

- **Task 1b:**  
  Each JSON includes `"title"`, `"outline"`, `"extracted_sections"`, and `"subsection_analysis"` — all per PDF.

## 🏁 Tips

- **Run one collection at a time for Task 1b.** Judges expect this—and it allows QA per-step.
- **Outputs are always per-PDF in the chosen output folder.**
- **If using Docker, always use PowerShell backtick (\`) for line breaks on Windows.**
- **No separate Task 2 script needed. Task 1b supports all persona-collection outputs.**
- **Scripts and Dockerfile are CPU-only, offline, and run under 60 seconds for standard collection sizes.**

## 🧪 Testing

Sample outputs are under `outputs/`. For correctness, review the extracted JSONs or use your own test script.
#
