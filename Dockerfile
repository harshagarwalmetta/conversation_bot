FROM ubuntu:22.04

# Install system dependencies
RUN apt-get update && apt-get install -y \
    curl \
    python3.10 \
    python3-pip \
    && rm -rf /var/lib/apt/lists/*

# Install Ollama
RUN curl -fsSL https://ollama.com/install.sh | sh

# Set up application directory
WORKDIR /app
COPY rebrand-conversational-chatbot .

# Install Python dependencies
RUN pip3 install --no-cache-dir -r requirements.txt

# Expose ports
EXPOSE 8000 11434

# Start script
RUN chmod +x start.sh
CMD ["./start.sh"]