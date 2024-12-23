from sqlalchemy.orm import Session
from app.models import Document


def create_document(db: Session, title: str, file_path: str) -> Document:
    """
    Create a new document record.

    Args:
        db (Session): The database session.
        title (str): The title of the document.
        file_path (str): The file path of the uploaded document.

    Returns:
        Document: The created document object.
    """
    document = Document(title=title, file_path=file_path, is_processed=False)
    db.add(document)
    db.commit()
    db.refresh(document)
    return document
