from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
from sqlalchemy.orm import Session
from pathlib import Path
import aiofiles
import tempfile

from ..config.settings import settings
from ..services.document_processor.document_processor import DocumentProcessor
from ..data.repositories.document_repository import DocumentRepository
from ..data.models.document import Base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Database setup
engine = create_engine(settings.final_database_url)
Base.metadata.create_all(bind=engine)
SessionLocal = sessionmaker(autocommit=False, autoload=True, bind=engine)

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/upload")
async def upload_file(
    file: UploadFile = File(...),
    enhance_with_ai: bool = True,
    db: Session = Depends(get_db)
):
    # Validate file extension
    file_extension = Path(file.filename).suffix.lower()[1:]
    if file_extension not in settings.SUPPORTED_FORMATS:
        raise HTTPException(
            status_code=400,
            detail=f"Unsupported file format. Supported formats: {settings.SUPPORTED_FORMATS}"
        )

    # Create temporary file
    with tempfile.NamedTemporaryFile(delete=False, suffix=Path(file.filename).suffix) as temp_file:
        # Write uploaded file to temporary file
        async with aiofiles.open(temp_file.name, 'wb') as out_file:
            content = await file.read()
            await out_file.write(content)
        
        # Process the file
        document_repository = DocumentRepository(db)
        processor = DocumentProcessor(document_repository)
        
        try:
            doc_id = processor.process_file(
                Path(temp_file.name),
                enhance_with_ai
            )
            
            if doc_id:
                return {"status": "success", "document_id": doc_id}
            else:
                raise HTTPException(
                    status_code=500,
                    detail="Failed to process the document"
                )
                
        finally:
            # Clean up temporary file
            Path(temp_file.name).unlink(missing_ok=True)

@router.post("/process-directory")
async def process_directory(
    directory_path: str,
    enhance_with_ai: bool = True,
    db: Session = Depends(get_db)
):
    path = Path(directory_path)
    if not path.exists() or not path.is_dir():
        raise HTTPException(
            status_code=400,
            detail=f"Directory not found: {directory_path}"
        )

    document_repository = DocumentRepository(db)
    processor = DocumentProcessor(document_repository)
    
    try:
        doc_ids = processor.process_directory(path, enhance_with_ai)
        return {
            "status": "success",
            "processed_documents": len(doc_ids),
            "document_ids": doc_ids
        }
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to process directory: {str(e)}"
        )

@router.get("/document/{document_id}")
async def get_document(document_id: int, db: Session = Depends(get_db)):
    document_repository = DocumentRepository(db)
    document = document_repository.get_by_id(document_id)
    
    if not document:
        raise HTTPException(
            status_code=404,
            detail=f"Document not found with id: {document_id}"
        )
        
    return {
        "id": document.id,
        "filename": document.filename,
        "file_type": document.file_type,
        "content": document.content,
        "created_at": document.created_at,
        "updated_at": document.updated_at
    }
