from fastapi import FastAPI
from app.database import Base, engine
from app.models import Message, Document, DocumentPage
from app.routers.messages import router as messages_router
from app.routers.documents import router as documents_router

# Initialize the FastAPI application
app = FastAPI(title="Conversational AI Platform", version="1.0")
app.include_router(messages_router)
app.include_router(documents_router)

# Automatically create tables
Base.metadata.create_all(bind=engine)

@app.get("/")
def read_root():
    return {"message": "Welcome to the Conversational AI Platform!"}
