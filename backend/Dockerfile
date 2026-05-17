FROM node:18-slim

# Install Python and dependencies
RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    tesseract-ocr \
    libgl1-mesa-glx \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Install Python packages
COPY requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt

# Install Node packages
COPY package*.json ./
RUN npm install

# Copy application code
COPY . .

# Ensure upload/output directories exist
RUN mkdir -p uploads outputs

EXPOSE 5000

CMD ["npm", "start"]
