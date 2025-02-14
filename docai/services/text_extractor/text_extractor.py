from typing import Optional
import PyPDF2
from docx import Document as DocxDocument
from openpyxl import load_workbook
from PIL import Image
import pytesseract
from pathlib import Path
import io

class TextExtractor:
    @staticmethod
    def extract_from_pdf(file_path: Path) -> str:
        text = ""
        with open(file_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            for page in pdf_reader.pages:
                text += page.extract_text() + "\n"
        return text.strip()

    @staticmethod
    def extract_from_docx(file_path: Path) -> str:
        doc = DocxDocument(file_path)
        return "\n".join([paragraph.text for paragraph in doc.paragraphs])

    @staticmethod
    def extract_from_xlsx(file_path: Path) -> str:
        wb = load_workbook(filename=file_path, read_only=True)
        text = []
        for sheet in wb.sheetnames:
            ws = wb[sheet]
            for row in ws.iter_rows():
                row_text = " ".join(str(cell.value) for cell in row if cell.value is not None)
                if row_text:
                    text.append(row_text)
        return "\n".join(text)

    @staticmethod
    def extract_from_image(file_path: Path) -> str:
        image = Image.open(file_path)
        return pytesseract.image_to_string(image)

    def extract_text(self, file_path: Path) -> Optional[str]:
        file_extension = file_path.suffix.lower()
        
        extractors = {
            '.pdf': self.extract_from_pdf,
            '.docx': self.extract_from_docx,
            '.xlsx': self.extract_from_xlsx,
            '.png': self.extract_from_image,
            '.jpg': self.extract_from_image,
            '.jpeg': self.extract_from_image,
        }
        
        extractor = extractors.get(file_extension)
        if not extractor:
            raise ValueError(f"Unsupported file type: {file_extension}")
            
        return extractor(file_path)
