#!/bin/bash

# Start Ollama in background
ollama serve &

# Wait for Ollama to initialize
sleep 5

# Pull required models
ollama pull llama3.2
ollama pull nomic-embed-text

# Start FastAPI
uvicorn app.main:app --host 0.0.0.0 --port 8000