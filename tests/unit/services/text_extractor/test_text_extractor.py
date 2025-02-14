import pytest
from pathlib import Path
from docai.services.text_extractor.text_extractor import TextExtractor

@pytest.fixture
def mock_pdf_file(tmp_path):
    pdf_content = b"%PDF-1.3\n1 0 obj\n<</Type/Catalog/Pages 2 0 R>>\nendobj\n2 0 obj\n<</Type/Pages/Kids[3 0 R]/Count 1>>\nendobj\n3 0 obj\n<</Type/Page/Parent 2 0 R/Resources<</Font<</F1<</Type/Font/Subtype/Type1/BaseFont/Helvetica>>>>>/Contents 4 0 R>>\nendobj\n4 0 obj\n<</Length 44>>stream\nBT /F1 12 Tf 72 712 Td (This is a test PDF document) Tj ET\nendstream\nendobj\nxref\n0 5\n0000000000 65535 f\n0000000009 00000 n\n0000000052 00000 n\n0000000101 00000 n\n0000000200 00000 n\ntrailer\n<</Size 5/Root 1 0 R>>\nstartxref\n292\n%%EOF"
    pdf_file = tmp_path / "test.pdf"
    pdf_file.write_bytes(pdf_content)
    return pdf_file

def test_extract_from_pdf(text_extractor, mock_pdf_file):
    """Test PDF text extraction"""
    text = text_extractor.extract_from_pdf(mock_pdf_file)
    assert "This is a test PDF document" in text

@pytest.fixture
def mock_docx_file(tmp_path):
    from docx import Document
    doc = Document()
    doc.add_paragraph("This is a test Word document")
    docx_file = tmp_path / "test.docx"
    doc.save(docx_file)
    return docx_file

def test_extract_from_docx(text_extractor, mock_docx_file):
    """Test DOCX text extraction"""
    text = text_extractor.extract_from_docx(mock_docx_file)
    assert "This is a test Word document" in text

def test_extract_text_with_unsupported_format(text_extractor):
    """Test handling of unsupported file format"""
    with pytest.raises(ValueError) as exc_info:
        text_extractor.extract_text(Path("test.unsupported"))
    assert "Unsupported file type" in str(exc_info.value)

def test_extract_text_with_nonexistent_file(text_extractor):
    """Test handling of non-existent file"""
    with pytest.raises(FileNotFoundError):
        text_extractor.extract_text(Path("nonexistent.pdf"))
