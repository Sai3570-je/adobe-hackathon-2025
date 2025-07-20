# Batch to run process_pdfs_1b.py for all collections using Docker
# Run from submission folder

cd C:\Users\saiph\Downloads\final_submission\submission

Write-Output "Processing Collection 1 with Docker..."
docker run --rm `
  -v "$PWD/data/sample_pdfs/task2/Collection 1/PDFs:/app/input" `
  -v "$PWD/outputs/1b_outputs:/app/output" `
  --network none `
  adobehackathon2025 `
  python process_pdfs_1b.py --input /app/input --output /app/output/Collection1 --persona "Travel Planner" --job "Plan a trip of 4 days for a group of 10 college friends."

Write-Output "Processing Collection 2 with Docker..."
docker run --rm `
  -v "$PWD/data/sample_pdfs/task2/Collection 2/PDFs:/app/input" `
  -v "$PWD/outputs/1b_outputs:/app/output" `
  --network none `
  adobehackathon2025 `
  python process_pdfs_1b.py --input /app/input --output /app/output/Collection2 --persona "Investment Analyst" --job "Analyze revenue trends, R&D investments, and market positioning strategies"

Write-Output "Processing Collection 3 with Docker..."
docker run --rm `
  -v "$PWD/data/sample_pdfs/task2/Collection 3/PDFs:/app/input" `
  -v "$PWD/outputs/1b_outputs:/app/output" `
  --network none `
  adobehackathon2025 `
  python process_pdfs_1b.py --input /app/input --output /app/output/Collection3 --persona "Undergraduate Chemistry Student" --job "Identify key concepts and mechanisms for exam preparation on reaction kinetics"

Write-Output "All collections processed with Docker! Check outputs/1b_outputs/ for folders with JSON files."
