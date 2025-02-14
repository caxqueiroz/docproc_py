import pytest
from pathlib import Path
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from docai.data.models.document import Base
from docai.data.repositories.document_repository import DocumentRepository
from docai.services.text_extractor.text_extractor import TextExtractor
from docai.services.ai_processor.ai_processor import AIProcessor
from docai.services.document_processor.document_processor import DocumentProcessor

@pytest.fixture
def test_db():
    """Create a test database"""
    engine = create_engine("sqlite:///./test.db")
    Base.metadata.create_all(engine)
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=True, bind=engine)
    
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()
        Path("./test.db").unlink(missing_ok=True)

@pytest.fixture
def document_repository(test_db):
    """Create a document repository instance"""
    return DocumentRepository(test_db)

@pytest.fixture
def text_extractor():
    """Create a text extractor instance"""
    return TextExtractor()

@pytest.fixture
def ai_processor():
    """Create an AI processor instance"""
    return AIProcessor()

@pytest.fixture
def document_processor(document_repository):
    """Create a document processor instance"""
    return DocumentProcessor(document_repository)

@pytest.fixture
def mock_env_openai_key(monkeypatch):
    """Mock OpenAI API key"""
    monkeypatch.setenv("OPENAI_API_KEY", "test_key")

@pytest.fixture
def mock_pdf_file(tmp_path):
    """Create a mock PDF file"""
    pdf_content = b"%PDF-1.3\n1 0 obj\n<</Type/Catalog/Pages 2 0 R>>\nendobj\n2 0 obj\n<</Type/Pages/Kids[3 0 R]/Count 1>>\nendobj\n3 0 obj\n<</Type/Page/Parent 2 0 R/Resources<</Font<</F1<</Type/Font/Subtype/Type1/BaseFont/Helvetica>>>>>/Contents 4 0 R>>\nendobj\n4 0 obj\n<</Length 44>>stream\nBT /F1 12 Tf 72 712 Td (This is a test PDF document) Tj ET\nendstream\nendobj\nxref\n0 5\n0000000000 65535 f\n0000000009 00000 n\n0000000052 00000 n\n0000000101 00000 n\n0000000200 00000 n\ntrailer\n<</Size 5/Root 1 0 R>>\nstartxref\n292\n%%EOF"
    pdf_file = tmp_path / "test.pdf"
    pdf_file.write_bytes(pdf_content)
    return pdf_file

@pytest.fixture
def mock_docx_file(tmp_path):
    """Create a mock DOCX file"""
    from docx import Document
    doc = Document()
    doc.add_paragraph("This is a test Word document")
    docx_file = tmp_path / "test.docx"
    doc.save(docx_file)
    return docx_file

@pytest.fixture
def test_files():
    """Get paths to test files"""
    fixtures_dir = Path(__file__).parent / "fixtures"
    return {
        "pdf": fixtures_dir / "sample.pdf",
        "docx": fixtures_dir / "sample.docx",
        "image": fixtures_dir / "sample.png"
    }
