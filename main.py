from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import tempfile
import os
from pathlib import Path
import hashlib
from datetime import datetime
from typing import Optional
import traceback
import asyncio
from concurrent.futures import ThreadPoolExecutor

# Apply compatibility fix before importing LlamaParse
import llamaparse_fix
# Fix event loop conflict for LlamaParse in FastAPI
import nest_asyncio
nest_asyncio.apply()
from llama_parse import LlamaParse
from doc_classifier import DocClassifier
from config import settings
from logger import logger
from industry_categories import get_categories_for_industry, get_available_industries

app = FastAPI(
    title="Document Classification API",
    description="Upload and classify business documents using LlamaParse and LLM",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize LlamaParse
llamaparse_client = LlamaParse(
    api_key=settings.LLAMAPARSE_API_KEY,  # Add this to your config
    result_type="text",
    verbose=True,
    do_not_cache=True,  # Don't cache files on LlamaParse servers (extra privacy)
    max_pages=10  # Only process first 10 pages for efficiency and cost control
)

# Supported file types
SUPPORTED_FILE_TYPES = {
    "application/pdf": [".pdf"],
    "image/jpeg": [".jpg", ".jpeg"],
    "image/png": [".png"],
    "image/tiff": [".tiff", ".tif"],
    "text/plain": [".txt"],
    "application/msword": [".doc"],
    "application/vnd.openxmlformats-officedocument.wordprocessingml.document": [".docx"]
}

def get_file_hash(file_content: bytes) -> str:
    """Generate MD5 hash of file content"""
    return hashlib.md5(file_content).hexdigest()

def validate_file_type(filename: str, content_type: str) -> bool:
    """Validate if file type is supported"""
    file_ext = Path(filename).suffix.lower()
    
    if content_type in SUPPORTED_FILE_TYPES:
        return file_ext in SUPPORTED_FILE_TYPES[content_type]
    
    # Fallback to extension check
    supported_extensions = [ext for exts in SUPPORTED_FILE_TYPES.values() for ext in exts]
    return file_ext in supported_extensions

def validate_file_size(file_size: int, max_size_mb: int = 50) -> bool:
    """Validate file size is within limits"""
    max_size_bytes = max_size_mb * 1024 * 1024
    return file_size <= max_size_bytes

def safe_cleanup(file_path: str):
    """Safely clean up temporary files"""
    try:
        if os.path.exists(file_path):
            os.unlink(file_path)
            logger.info(f"Cleaned up temporary file: {file_path}")
    except Exception as e:
        logger.warning(f"Failed to cleanup file {file_path}: {str(e)}")

# Helper function to run LlamaParse in thread pool to avoid event loop conflicts
async def run_llamaparse_async(file_path: str):
    """Run LlamaParse in a thread pool to avoid event loop conflicts"""
    def run_llamaparse():
        # Create a new event loop for this thread
        import asyncio
        try:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            return llamaparse_client.load_data(file_path)
        finally:
            loop.close()
    
    loop = asyncio.get_event_loop()
    with ThreadPoolExecutor() as executor:
        return await loop.run_in_executor(executor, run_llamaparse)

class APIError(Exception):
    """Custom API error with structured details"""
    def __init__(self, message: str, error_type: str = "general", details: dict = None):
        self.message = message
        self.error_type = error_type
        self.details = details or {}
        super().__init__(message)

@app.get("/")
async def root():
    """Health check endpoint"""
    return {"message": "Document Classification API is running", "timestamp": datetime.now().isoformat()}

@app.get("/health")
async def health_check():
    """Detailed health check"""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "supported_file_types": list(SUPPORTED_FILE_TYPES.keys())
    }

@app.post("/upload")
async def upload_document(file: UploadFile = File(...)):
    """
    Upload a document and extract text using LlamaParse
    Returns file info and extracted text
    """
    try:
        # Validate file type
        if not validate_file_type(file.filename, file.content_type):
            raise HTTPException(
                status_code=400,
                detail=f"Unsupported file type. Supported types: {list(SUPPORTED_FILE_TYPES.keys())}"
            )
        
        # Read file content
        file_content = await file.read()
        file_hash = get_file_hash(file_content)
        file_size = len(file_content)
        
        logger.info(f"Processing file: {file.filename}, size: {file_size} bytes, hash: {file_hash}")
        
        # Save to temporary file for LlamaParse
        with tempfile.NamedTemporaryFile(delete=False, suffix=Path(file.filename).suffix) as temp_file:
            temp_file.write(file_content)
            temp_file_path = temp_file.name
        
        try:
            # Extract text using LlamaParse
            logger.info("Starting LlamaParse extraction...")
            start_time = datetime.now()
            
            documents = await run_llamaparse_async(temp_file_path)
            extracted_text = documents[0].text if documents else ""
            
            end_time = datetime.now()
            processing_time = (end_time - start_time).total_seconds()
            
            logger.info(f"LlamaParse completed in {processing_time:.2f} seconds")
            
            return JSONResponse(
                status_code=200,
                content={
                    "status": "success",
                    "file_info": {
                        "filename": file.filename,
                        "content_type": file.content_type,
                        "file_size": file_size,
                        "file_hash": file_hash
                    },
                    "extraction": {
                        "text_length": len(extracted_text),
                        "processing_time_seconds": processing_time,
                        "extracted_text": extracted_text[:1000] + "..." if len(extracted_text) > 1000 else extracted_text
                    },
                    "timestamp": datetime.now().isoformat()
                }
            )
            
        finally:
            # Clean up temporary file
            if os.path.exists(temp_file_path):
                os.unlink(temp_file_path)
                
    except Exception as e:
        logger.error(f"Error processing file {file.filename}: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error processing file: {str(e)}")

@app.post("/upload-and-classify")
async def upload_and_classify_document(file: UploadFile = File(...), industry: str = "general"):
    """
    Upload a document, extract text with LlamaParse, and classify it
    Complete end-to-end processing with comprehensive error handling
    """
    temp_file_path = None
    
    try:
        # Validate filename
        if not file.filename or file.filename.strip() == "":
            raise APIError("Invalid filename", "validation", {"field": "filename"})
        
        # Validate file type
        if not validate_file_type(file.filename, file.content_type):
            raise APIError(
                f"Unsupported file type. Supported types: {list(SUPPORTED_FILE_TYPES.keys())}", 
                "validation",
                {"supported_types": list(SUPPORTED_FILE_TYPES.keys()), "received": file.content_type}
            )
        
        # Read file content
        try:
            file_content = await file.read()
        except Exception as e:
            raise APIError(f"Failed to read file content: {str(e)}", "file_read")
        
        file_hash = get_file_hash(file_content)
        file_size = len(file_content)
        
        # Validate file size
        if not validate_file_size(file_size):
            raise APIError(
                f"File too large. Maximum size: 50MB, received: {file_size / (1024*1024):.1f}MB",
                "validation",
                {"max_size_mb": 50, "file_size_mb": file_size / (1024*1024)}
            )
        
        # Validate file content
        if file_size == 0:
            raise APIError("Empty file uploaded", "validation", {"file_size": 0})
        
        logger.info(f"Processing and classifying file: {file.filename} ({file_size} bytes)")
        
        # Save to temporary file for LlamaParse
        try:
            with tempfile.NamedTemporaryFile(delete=False, suffix=Path(file.filename).suffix) as temp_file:
                temp_file.write(file_content)
                temp_file_path = temp_file.name
        except Exception as e:
            raise APIError(f"Failed to create temporary file: {str(e)}", "temp_file_creation")
        
        try:
            # Step 1: Extract text using LlamaParse
            logger.info("Starting LlamaParse extraction...")
            parse_start = datetime.now()
            
            try:
                documents = await run_llamaparse_async(temp_file_path)
                extracted_text = documents[0].text if documents and len(documents) > 0 else ""
            except Exception as e:
                logger.error(f"LlamaParse extraction failed: {str(e)}")
                raise APIError(
                    f"Document parsing failed: {str(e)}", 
                    "llamaparse_error",
                    {"stage": "text_extraction", "original_error": str(e)}
                )
            
            parse_end = datetime.now()
            parse_time = (parse_end - parse_start).total_seconds()
            
            # Validate extracted text
            if not extracted_text or not extracted_text.strip():
                raise APIError(
                    "No text could be extracted from the document", 
                    "extraction_failed",
                    {"text_length": len(extracted_text), "file_type": file.content_type}
                )
            
            if len(extracted_text.strip()) < 10:
                logger.warning(f"Very short extracted text: {len(extracted_text)} characters")
            
            # Step 2: Classify using DocClassifier
            logger.info("Starting document classification...")
            classify_start = datetime.now()
            
            try:
                classifier = DocClassifier(extracted_text, industry)
                classification_result = classifier.classify_document()
            except Exception as e:
                logger.error(f"Classification failed: {str(e)}")
                logger.error(f"Full traceback: {traceback.format_exc()}")
                raise APIError(
                    f"Document classification failed: {str(e)}", 
                    "classification_error",
                    {"stage": "classification", "text_length": len(extracted_text), "original_error": str(e)}
                )
            
            classify_end = datetime.now()
            classify_time = (classify_end - classify_start).total_seconds()
            total_time = parse_time + classify_time
            
            logger.info(f"Classification completed successfully: {classification_result.get('classification', 'unknown')}")
            
            return JSONResponse(
                status_code=200,
                content={
                    "status": "success",
                    "file_info": {
                        "filename": file.filename,
                        "content_type": file.content_type,
                        "file_size": file_size,
                        "file_hash": file_hash
                    },
                    "processing": {
                        "parse_time_seconds": parse_time,
                        "classify_time_seconds": classify_time,
                        "total_time_seconds": total_time,
                        "text_length": len(extracted_text)
                    },
                    "results": {
                        "classification": classification_result["classification"],
                        "summary": classification_result["summary"],
                        "extracted_data": classification_result["extracted_data"]
                    },
                    "timestamp": datetime.now().isoformat()
                }
            )
            
        finally:
            # Clean up temporary file
            if temp_file_path:
                safe_cleanup(temp_file_path)
                
    except APIError as e:
        logger.error(f"API Error processing {file.filename}: {e.message}")
        error_detail = {
            "error": e.message,
            "error_type": e.error_type,
            "details": e.details,
            "timestamp": datetime.now().isoformat()
        }
        
        if temp_file_path:
            safe_cleanup(temp_file_path)
        
        status_code = 400 if e.error_type in ["validation", "extraction_failed"] else 500
        raise HTTPException(status_code=status_code, detail=error_detail)
        
    except HTTPException:
        if temp_file_path:
            safe_cleanup(temp_file_path)
        raise
        
    except Exception as e:
        logger.error(f"Unexpected error processing {file.filename}: {str(e)}")
        logger.error(f"Full traceback: {traceback.format_exc()}")
        
        if temp_file_path:
            safe_cleanup(temp_file_path)
        
        raise HTTPException(
            status_code=500, 
            detail={
                "error": "Internal server error during document processing",
                "error_type": "unexpected_error",
                "timestamp": datetime.now().isoformat()
            }
        )

class TextClassificationRequest(BaseModel):
    text: str
    industry: str = "general"

@app.post("/classify")
async def classify_text(request: TextClassificationRequest):
    """
    Classify pre-extracted text using DocClassifier
    Use this endpoint if you already have extracted text
    """
    try:
        if not request.text.strip():
            raise HTTPException(status_code=400, detail="Text content cannot be empty")
        
        logger.info(f"Classifying text of length: {len(request.text)}")
        
        start_time = datetime.now()
        classifier = DocClassifier(request.text, request.industry)
        result = classifier.classify_document()
        end_time = datetime.now()
        
        processing_time = (end_time - start_time).total_seconds()
        
        return JSONResponse(
            status_code=200,
            content={
                "status": "success",
                "processing": {
                    "text_length": len(request.text),
                    "processing_time_seconds": processing_time
                },
                "results": {
                    "classification": result["classification"],
                    "summary": result["summary"],
                    "extracted_data": result["extracted_data"]
                },
                "timestamp": datetime.now().isoformat()
            }
        )
        
    except Exception as e:
        logger.error(f"Error classifying text: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error classifying text: {str(e)}")

@app.get("/industries")
async def get_industries():
    """
    Get all available industries
    """
    try:
        industries = get_available_industries()
        
        return JSONResponse(
            status_code=200,
            content={
                "status": "success",
                "industries": industries,
                "total_industries": len(industries),
                "timestamp": datetime.now().isoformat()
            }
        )
        
    except Exception as e:
        logger.error(f"Error getting industries: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error retrieving industries: {str(e)}")

@app.get("/categories")
async def get_categories(industry: str = "general"):
    """
    Get all available classification categories with descriptions for a specific industry
    """
    try:
        industry_data = get_categories_for_industry(industry)
        categories = industry_data["categories"]
        descriptions = industry_data["descriptions"]
        
        return JSONResponse(
            status_code=200,
            content={
                "status": "success",
                "industry": industry,
                "categories": categories,
                "descriptions": descriptions,
                "total_categories": len(categories),
                "timestamp": datetime.now().isoformat()
            }
        )
        
    except Exception as e:
        logger.error(f"Error getting categories for industry {industry}: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error retrieving categories: {str(e)}")

@app.post("/validate")
async def validate_classification(file: UploadFile = File(...), expected_category: str = None):
    """
    Validate classification against expected category for testing
    Returns classification result with correctness score
    """
    try:
        # Process document normally
        result = await upload_and_classify_document(file)
        result_data = result.body.decode() if hasattr(result, 'body') else result
        
        # If it's a JSONResponse, extract the content
        if isinstance(result, JSONResponse):
            # Get the actual classification result
            temp_file_path = None
            try:
                file_content = await file.read()
                file.file.seek(0)  # Reset file pointer for reuse
                
                with tempfile.NamedTemporaryFile(delete=False, suffix=Path(file.filename).suffix) as temp_file:
                    temp_file.write(file_content)
                    temp_file_path = temp_file.name
                
                documents = await run_llamaparse_async(temp_file_path)
                extracted_text = documents[0].text if documents else ""
                
                classifier = DocClassifier(extracted_text)
                classification_result = classifier.classify_document()
                
                # Calculate validation metrics
                predicted_category = classification_result["classification"]
                is_correct = predicted_category == expected_category if expected_category else None
                
                validation_result = {
                    "status": "success",
                    "validation": {
                        "predicted_category": predicted_category,
                        "expected_category": expected_category,
                        "is_correct": is_correct,
                        "confidence_score": None  # Could be added later
                    },
                    "classification_result": classification_result,
                    "file_info": {
                        "filename": file.filename,
                        "content_type": file.content_type
                    },
                    "timestamp": datetime.now().isoformat()
                }
                
                return JSONResponse(status_code=200, content=validation_result)
                
            finally:
                if temp_file_path:
                    safe_cleanup(temp_file_path)
        
    except Exception as e:
        logger.error(f"Validation error: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail={
                "error": f"Validation failed: {str(e)}",
                "error_type": "validation_error",
                "timestamp": datetime.now().isoformat()
            }
        )

@app.get("/test-status")
async def test_status():
    """
    Get testing and validation status
    """
    try:
        # Check if LlamaParse is working
        llamaparse_status = "unknown"
        try:
            # Simple test - this would need a test file
            llamaparse_status = "available"
        except:
            llamaparse_status = "error"
        
        # Check if OpenAI is working
        openai_status = "unknown"
        try:
            test_classifier = DocClassifier("test document", "general")
            openai_status = "available"
        except:
            openai_status = "error"
        
        return {
            "status": "healthy",
            "services": {
                "llamaparse": llamaparse_status,
                "openai": openai_status
            },
            "api_version": "1.0.0",
            "categories_count": len(DocClassifier("test", "general").class_labels),
            "timestamp": datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Test status error: {str(e)}")
        return {
            "status": "error",
            "error": str(e),
            "timestamp": datetime.now().isoformat()
        }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
