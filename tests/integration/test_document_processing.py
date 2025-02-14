import pytest
from pathlib import Path
from docai.services.document_processor.document_processor import DocumentProcessor
from docai.data.repositories.document_repository import DocumentRepository

def test_end_to_end_document_processing(test_db, mock_pdf_file, mock_docx_file):
    """Test the entire document processing pipeline"""
    # Setup
    document_repository = DocumentRepository(test_db)
    processor = DocumentProcessor(document_repository)
    
    # Process PDF
    pdf_doc_id = processor.process_file(mock_pdf_file)
    pdf_doc = document_repository.get_by_id(pdf_doc_id)
    assert "test PDF document" in pdf_doc.content
    
    # Process DOCX
    docx_doc_id = processor.process_file(mock_docx_file)
    docx_doc = document_repository.get_by_id(docx_doc_id)
    assert "test Word document" in docx_doc.content
    
    # Verify storage
    assert Path(pdf_doc.storage_path).exists()
    assert Path(docx_doc.storage_path).exists()

def test_batch_processing(test_db, mock_pdf_file, mock_docx_file):
    """Test processing multiple files in a directory"""
    # Setup
    document_repository = DocumentRepository(test_db)
    processor = DocumentProcessor(document_repository)
    
    # Process directory
    test_dir = mock_pdf_file.parent
    doc_ids = processor.process_directory(test_dir)
    
    # Verify results
    assert len(doc_ids) > 0
    for doc_id in doc_ids:
        doc = document_repository.get_by_id(doc_id)
        assert doc.content is not None
        assert Path(doc.storage_path).exists()

def test_ai_enhancement_integration(test_db, mock_pdf_file, mock_env_openai_key):
    """Test integration with AI enhancement"""
    # Setup
    document_repository = DocumentRepository(test_db)
    processor = DocumentProcessor(document_repository)
    
    # Process with AI enhancement
    doc_id = processor.process_file(mock_pdf_file, enhance_with_ai=True)
    doc = document_repository.get_by_id(doc_id)
    
    # Verify AI enhancement
    assert doc.content is not None
    assert len(doc.content) > 0
