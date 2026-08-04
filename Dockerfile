# Start from an official Python 3.10 base image (matches our local venv version)
FROM python:3.10-slim

# Set the working directory inside the container
WORKDIR /app

# Copy just the requirements file first (for efficient caching)
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the project files into the container
COPY . .

# Command to run when the container starts
CMD ["python", "ai_extract.py"]