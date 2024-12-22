from sqlalchemy.orm import Session
from app.models import Message

def create_message(db: Session, content: str, is_ai: bool) -> Message:
    """
    Create a new message record.

    Args:
        db (Session): The database session.
        content (str): The content of the message.
        is_ai (bool): Indicates whether the message is from the AI or the user.

    Returns:
        Message: The created message object.
    """
    message = Message(content=content, is_ai=is_ai)
    db.add(message)
    db.commit()
    db.refresh(message)
    return message

def get_all_messages(db: Session) -> list[Message]:
    """
    Retrieve all messages from the database.

    Args:
        db (Session): The database session.

    Returns:
        list[Message]: A list of all message objects.
    """
    return db.query(Message).all()
