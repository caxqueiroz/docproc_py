import pytest
from pathlib import Path
from unittest.mock import Mock, patch
from docai.services.document_processor.document_processor import DocumentProcessor

@pytest.fixture
def mock_text_extractor():
    """Mock text extractor"""
    mock = Mock()
    mock.extract_text.return_value = "Extracted text content"
    return mock

@pytest.fixture
def mock_ai_processor():
    """Mock AI processor"""
    mock = Mock()
    mock.enhance_extraction.return_value = "Enhanced text content"
    return mock

def test_process_file(document_processor, mock_pdf_file):
    """Test processing a single file"""
    doc_id = document_processor.process_file(mock_pdf_file)
    assert doc_id is not None

def test_process_file_with_ai_enhancement(document_processor, mock_pdf_file, mock_env_openai_key):
    """Test processing a file with AI enhancement"""
    doc_id = document_processor.process_file(mock_pdf_file, enhance_with_ai=True)
    assert doc_id is not None

def test_process_nonexistent_file(document_processor):
    """Test handling of non-existent file"""
    with pytest.raises(FileNotFoundError):
        document_processor.process_file(Path("nonexistent.pdf"))

def test_process_directory(document_processor, mock_pdf_file, mock_docx_file):
    """Test processing a directory of files"""
    test_dir = mock_pdf_file.parent
    doc_ids = document_processor.process_directory(test_dir)
    assert len(doc_ids) > 0

def test_process_nonexistent_directory(document_processor):
    """Test handling of non-existent directory"""
    with pytest.raises(NotADirectoryError):
        document_processor.process_directory(Path("nonexistent_dir"))

def test_store_file(document_processor, mock_pdf_file):
    """Test file storage functionality"""
    stored_path = document_processor._store_file(mock_pdf_file, mock_pdf_file.name)
    assert stored_path.exists()
    assert stored_path.is_file()
