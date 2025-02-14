# Document AI Processor

A modular Python application for processing various document types (PDF, DOCX, XLSX, images) and extracting their content using OCR and AI enhancement.

## Features

- Support for multiple file formats (PDF, DOCX, XLSX, PNG, JPG, JPEG)
- Text extraction with OCR capabilities
- AI-powered text enhancement using OpenAI GPT-4
- REST API endpoints for file upload and processing
- Batch processing of directories
- SQLite database storage
- Modular architecture with separate layers (API, Service, Data)

## Prerequisites

- Python 3.8+
- Tesseract OCR
- OpenAI API key

## Installation

1. Install system dependencies:
```bash
# For macOS
brew install tesseract
```

2. Install Python dependencies:
```bash
pip install -r requirements.txt
```

3. Create a `.env` file in the project root with your configuration:
```env
# OpenAI
OPENAI_API_KEY=your_api_key_here

# Database
DATABASE_URL=sqlite:///./docai.db

# Storage
STORAGE_PATH=storage

# File Processing
MAX_FILE_SIZE=10485760  # 10MB in bytes

# API Configuration
API_HOST=0.0.0.0
API_PORT=8000
```

## Project Structure

```
docai/
├── api/
│   └── router.py
├── services/
│   ├── document_processor/
│   ├── text_extractor/
│   └── ai_processor/
├── data/
│   ├── models/
│   └── repositories/
├── config/
│   └── settings.py
└── storage/
```

## Usage

1. Start the server:
```bash
python -m docai.main
```

2. API Endpoints:

- POST `/upload`: Upload and process a single file
  ```bash
  curl -X POST -F "file=@document.pdf" http://localhost:8000/upload
  ```

- POST `/process-directory`: Process all supported files in a directory
  ```bash
  curl -X POST -H "Content-Type: application/json" \
       -d '{"directory_path": "/path/to/documents"}' \
       http://localhost:8000/process-directory
  ```

- GET `/document/{document_id}`: Retrieve processed document
  ```bash
  curl http://localhost:8000/document/1
  ```

## Configuration

All configuration is managed through environment variables, which can be set in the `.env` file:

| Variable | Description | Default Value |
|----------|-------------|---------------|
| `OPENAI_API_KEY` | Your OpenAI API key | Required |
| `DATABASE_URL` | Database connection URL | `sqlite:///./docai.db` |
| `STORAGE_PATH` | Path to store processed files | `storage` |
| `MAX_FILE_SIZE` | Maximum file size in bytes | `10485760` (10MB) |
| `API_HOST` | API server host | `0.0.0.0` |
| `API_PORT` | API server port | `8000` |

Supported file formats:
- PDF (`.pdf`)
- Word Documents (`.docx`)
- Excel Spreadsheets (`.xlsx`)
- Images (`.png`, `.jpg`, `.jpeg`)
