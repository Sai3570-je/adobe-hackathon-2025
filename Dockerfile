# Use official Python image and force AMD64 as per challenge requirement
FROM --platform=linux/amd64 python:3.10-slim

# Create an app directory inside the container
WORKDIR /app

# Copy code files and requirements
COPY src/ /app/
COPY src/requirements.txt /app/requirements.txt

# Install dependencies
RUN pip install --no-cache-dir -r /app/requirements.txt

# By default, execute Task 1b script (you can override this in `docker run`)
CMD ["python", "process_pdfs_1b.py", "--input", "/app/input", "--output", "/app/output"]
