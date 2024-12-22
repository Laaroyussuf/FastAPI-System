from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base

# Message Model
class Message(Base):
    """
    Represents a message exchanged in the conversational platform.

    Attributes:
        id (int): Primary key.
        is_ai (bool): Indicates if the message is from AI.
        content (str): Message content.
        timestamp (datetime): Time when the message was created.
    """
    __tablename__ = "messages"

    id = Column(Integer, primary_key=True, index=True)
    is_ai = Column(Boolean, default=False)
    content = Column(String, nullable=False)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())


# Document Model
class Document(Base):
    """
    Represents a document uploaded to the platform.

    Attributes:
        id (int): Primary key.
        title (str): Document title.
        file_path (str): Path to the document file.
        is_processed (bool): Indicates if the document is fully processed.
        pages (relationship): Relationship to associated document pages.
    """
    __tablename__ = "documents"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    file_path = Column(String, nullable=False)
    is_processed = Column(Boolean, default=False)

    # Relationship with DocumentPage
    pages = relationship("DocumentPage", back_populates="document")


# DocumentPage Model
class DocumentPage(Base):
    """
    Represents a page within a document.

    Attributes:
        id (int): Primary key.
        document_id (int): Foreign key referencing the document.
        page_number (int): Page number within the document.
        content (str): Text content of the page.
        is_processed (bool): Indicates if the page is processed.
        document (relationship): Relationship to the associated document.
    """
    __tablename__ = "document_pages"

    id = Column(Integer, primary_key=True, index=True)
    document_id = Column(Integer, ForeignKey("documents.id"), nullable=False)
    page_number = Column(Integer, nullable=False)
    content = Column(String, nullable=False)
    is_processed = Column(Boolean, default=False)

    # Relationship with Document
    document = relationship("Document", back_populates="pages")
