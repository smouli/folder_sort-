# Document Classification API

A FastAPI-based service that combines LlamaParse and OpenAI to classify business documents into categories and extract relevant information.

## Features

- 📄 **Document Upload**: Supports PDF, DOCX, images, and text files
- 🔍 **Text Extraction**: Uses LlamaParse for high-quality text extraction from complex documents
- 🏷️ **Smart Classification**: Classifies documents into 11 business categories using OpenAI
- 📊 **Data Extraction**: Extracts category-specific information from classified documents
- ⚡ **Fast API**: RESTful endpoints with automatic documentation

## Business Categories

- **Finance**: budgets, forecasts, invoices, audits
- **Legal**: contracts, compliance, IP, regulatory  
- **Operations**: process docs, logistics, supply chain, facilities
- **HR**: hiring, payroll, benefits, employee relations
- **Product**: roadmaps, specs, R&D, design
- **Engineering / Tech**: code, architecture, infrastructure, IT
- **Sales**: pitches, deal flow, pipeline, CRM exports
- **Marketing / Communications**: brand, PR, campaigns, content
- **Customer Success / Support**: onboarding, training, help docs, feedback
- **Strategy / Corp Dev**: M&A, partnerships, investor updates, OKRs
- **Compliance / Risk**: audit reports, security, regulatory filings

## API Endpoints

### `GET /` - Health Check
Basic health check endpoint.

### `GET /health` - Detailed Health Check
Returns API status and supported file types.

### `GET /categories` - Get Categories
Returns all available classification categories with descriptions.

### `POST /upload` - Upload Document
Upload a document and extract text using LlamaParse.

**Request**: Multipart form with file upload
**Response**: File info and extracted text (first 1000 chars)

### `POST /upload-and-classify` - Complete Pipeline
Upload a document, extract text, and classify it in one call.

**Request**: Multipart form with file upload
**Response**: Full classification results with extracted data

### `POST /classify` - Classify Text
Classify pre-extracted text.

**Request**: JSON with text field
**Response**: Classification results

## Setup

1. **Install dependencies**:
```bash
# For production (API only)
pip install -r requirements.txt

# For development (includes testing and evaluation tools)
pip install -r requirements-dev.txt
```

2. **Configure environment variables** by creating a `.env` file:
```bash
# Create .env file in project root
cat > .env << EOF
OPENAI_API_KEY=your_openai_api_key_here
LLAMAPARSE_API_KEY=your_llamaparse_api_key_here
USER_ID=your_user_id
EOF
```

Or set them as environment variables:
```bash
export OPENAI_API_KEY="your_openai_api_key"
export LLAMAPARSE_API_KEY="your_llamaparse_api_key"
```

3. **Run the API**:
```bash
python main.py
# or
uvicorn main:app --host 0.0.0.0 --port 8000
```

4. **Access the API**:
- API: http://localhost:8000
- Docs: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Usage Examples

### Upload and Classify a Document
```bash
curl -X POST "http://localhost:8000/upload-and-classify" \
  -H "accept: application/json" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@contract.pdf"
```

### Classify Text
```bash
curl -X POST "http://localhost:8000/classify" \
  -H "accept: application/json" \
  -H "Content-Type: application/json" \
  -d '{"text": "This is a master service agreement between..."}'
```

### Get Available Categories
```bash
curl -X GET "http://localhost:8000/categories"
```

## Response Format

```json
{
  "status": "success",
  "file_info": {
    "filename": "contract.pdf",
    "content_type": "application/pdf",
    "file_size": 150000,
    "file_hash": "abc123def456"
  },
  "processing": {
    "parse_time_seconds": 2.5,
    "classify_time_seconds": 1.2,
    "total_time_seconds": 3.7,
    "text_length": 5000
  },
  "results": {
    "classification": "Legal",
    "summary": "A master service agreement between Company A and Company B...",
    "extracted_data": {
      "document_type": "Legal",
      "extracted_info": "Document type: Contract\nParties: Company A, Company B\n..."
    }
  },
  "timestamp": "2024-01-15T10:30:00"
}
```

## Supported File Types

- **PDF**: `.pdf`
- **Word**: `.doc`, `.docx`
- **Images**: `.jpg`, `.jpeg`, `.png`, `.tiff`, `.tif`
- **Text**: `.txt`

## Architecture

1. **LlamaParse**: Extracts clean, structured text from uploaded documents
2. **DocClassifier**: Uses OpenAI GPT-4o-mini to classify and extract data
3. **FastAPI**: Provides RESTful endpoints with automatic validation and documentation
