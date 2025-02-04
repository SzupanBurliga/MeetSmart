FROM python:3.11.9-slim

# Install dependencies
RUN apt-get update && \
    apt-get install -y ffmpeg gcc libffi-dev && \
    apt-get clean

# Set the working directory
WORKDIR /app

# Copy the requirements file and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . .

# Expose the port the app runs on
EXPOSE 5000

# Run the application
CMD ["python", "main.py"]