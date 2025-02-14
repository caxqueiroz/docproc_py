import shutil
from pathlib import Path
from typing import Optional
from ...config.settings import settings
from ..text_extractor.text_extractor import TextExtractor
from ..ai_processor.ai_processor import AIProcessor
from ...data.repositories.document_repository import DocumentRepository

class DocumentProcessor:
    def __init__(self, document_repository: DocumentRepository):
        self.text_extractor = TextExtractor()
        self.ai_processor = AIProcessor()
        self.document_repository = document_repository
        self.storage_path = settings.final_storage_path
        self.storage_path.mkdir(exist_ok=True)

    def _store_file(self, file_path: Path, original_filename: str) -> Path:
        """Store the file in the storage directory with a unique name"""
        original_path = Path(original_filename)
        storage_filename = f"{original_path.stem}_{file_path.stat().st_mtime_ns}{original_path.suffix}"
        storage_file_path = self.storage_path / storage_filename
        shutil.copy2(file_path, storage_file_path)
        return storage_file_path

    def process_file(self, file_path: Path, enhance_with_ai: bool = True) -> Optional[int]:
        """Process a single file and return the document ID"""
        if not file_path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")

        # Store file
        stored_path = self._store_file(file_path, file_path.name)
        
        # Extract text
        try:
            extracted_text = self.text_extractor.extract_text(file_path)
            
            # Enhance with AI if requested and if text extraction might be poor
            if enhance_with_ai and extracted_text.strip():
                enhanced_text = self.ai_processor.enhance_extraction(
                    extracted_text,
                    file_path.suffix
                )
                final_text = enhanced_text
            else:
                final_text = extracted_text

            # Save to database
            document = self.document_repository.create(
                filename=file_path.name,
                file_type=file_path.suffix.lower()[1:],
                content=final_text,
                storage_path=str(stored_path)
            )
            
            return document.id
            
        except Exception as e:
            # In a production environment, you'd want to log this error
            print(f"Error processing file {file_path}: {str(e)}")
            return None

    def process_directory(self, directory_path: Path, enhance_with_ai: bool = True) -> list[int]:
        """Process all supported files in a directory"""
        if not directory_path.is_dir():
            raise NotADirectoryError(f"Not a directory: {directory_path}")

        processed_ids = []
        supported_extensions = set(settings.SUPPORTED_FORMATS)

        for file_path in directory_path.rglob("*"):
            if file_path.suffix.lower()[1:] in supported_extensions:
                doc_id = self.process_file(file_path, enhance_with_ai)
                if doc_id:
                    processed_ids.append(doc_id)

        return processed_ids
