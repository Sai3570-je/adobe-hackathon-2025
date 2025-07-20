#!/bin/bash

# Adobe India Hackathon 2025 - PDF Processing Solutions
# Sample script to run both Task 1a and Task 1b solutions

echo "Adobe India Hackathon 2025 - PDF Processing Solutions"
echo "======================================================"

# Check if Python is available
if ! command -v python3 &> /dev/null; then
    echo "Error: Python3 is not installed or not in PATH"
    exit 1
fi

# Install dependencies
echo "Installing dependencies..."
pip install -r src/requirements.txt

# Create output directories if they don't exist
mkdir -p outputs/1a_outputs
mkdir -p outputs/1b_outputs

# Run Task 1a
echo ""
echo "Running Task 1a solution..."
python3 src/process_pdfs_1a.py --input data/sample_pdfs/ --output outputs/1a_outputs/
if [ $? -eq 0 ]; then
    echo "Task 1a completed successfully!"
else
    echo "Task 1a failed!"
fi

# Run Task 1b
echo ""
echo "Running Task 1b solution..."
python3 src/process_pdfs_1b.py --input data/sample_pdfs/ --output outputs/1b_outputs/
if [ $? -eq 0 ]; then
    echo "Task 1b completed successfully!"
else
    echo "Task 1b failed!"
fi

echo ""
echo "All tasks completed. Check the outputs/ directory for results."

