from sqlalchemy.orm import Session
from ..models.document import Document
from datetime import datetime

class DocumentRepository:
    def __init__(self, db_session: Session):
        self.db_session = db_session

    def create(self, filename: str, file_type: str, content: str, storage_path: str) -> Document:
        document = Document(
            filename=filename,
            file_type=file_type,
            content=content,
            storage_path=storage_path
        )
        self.db_session.add(document)
        self.db_session.commit()
        self.db_session.refresh(document)
        return document

    def get_by_id(self, document_id: int) -> Document:
        return self.db_session.query(Document).filter(Document.id == document_id).first()

    def get_all(self):
        return self.db_session.query(Document).all()

    def update_content(self, document_id: int, content: str) -> Document:
        document = self.get_by_id(document_id)
        if document:
            document.content = content
            document.updated_at = datetime.utcnow()
            self.db_session.commit()
            self.db_session.refresh(document)
        return document
