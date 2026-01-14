# Step 1: Use official Python image
FROM python:3.11-slim

# Step 2: Set working directory inside container
WORKDIR /app

# Step 3: Copy dependency file
COPY requirements.txt .

# Step 4: Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Step 5: Copy project files
COPY src ./src
COPY config.py .
COPY credentials ./credentials

# Step 6: Default command
CMD ["python", "-m", "src.main"]
