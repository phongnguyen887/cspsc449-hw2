# Use official Python image
FROM python:3.10-slim

# Set the working directory
WORKDIR /app

# Copy dependencies
COPY requirements.txt requirements.txt

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the app code into the container
COPY . .

# Expose the application port
EXPOSE 8000

# Run the FastAPI app
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]