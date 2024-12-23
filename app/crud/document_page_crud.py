from sqlalchemy.orm import Session
from app.models import DocumentPage


def create_document_page(db: Session, document_id: int, page_number: int, content: str) -> DocumentPage:
    """
    Create a new document page record.

    Args:
        db (Session): The database session.
        document_id (int): The ID of the parent document.
        page_number (int): The page number of the document.
        content (str): The content of the page.

    Returns:
        DocumentPage: The created document page object.
    """
    page = DocumentPage(
        document_id=document_id,
        page_number=page_number,
        content=content,
        is_processed=False
    )
    db.add(page)
    db.commit()
    db.refresh(page)
    return page


def mark_page_as_processed(db: Session, page_id: int) -> DocumentPage:
    """
    Mark a document page as processed.

    Args:
        db (Session): The database session.
        page_id (int): The ID of the document page.

    Returns:
        DocumentPage: The updated document page object.
    """
    page = db.query(DocumentPage).filter(DocumentPage.id == page_id).first()
    if page:
        page.is_processed = True
        db.commit()
        db.refresh(page)
    return page