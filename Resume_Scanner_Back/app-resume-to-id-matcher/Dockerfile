# Start from a base image
FROM python:3.10-slim-buster

# Set the working directory
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt requirements.txt
RUN apt-get update && apt-get install -y \
    cmake \
    build-essential \
    libssl-dev \
    && rm -rf /var/lib/apt/lists/*

RUN apt-get update && \
    apt-get install -y libgl1-mesa-glx libglib2.0-0

RUN apt-get update && \
    apt-get install -y poppler-utils
    
# Install the required packages
RUN pip3 install --upgrade pip
RUN pip3 install face_recognition
RUN pip3 install -r requirements.txt

# Copy the application code into the container
COPY ["Resume_scanner.py", "app.py","./"] .

# Expose the app port
EXPOSE 8080

# Run command
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8080"]
