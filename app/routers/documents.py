import os
from fastapi import APIRouter, UploadFile, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.crud.document_crud import create_document
from app.crud.document_page_crud import create_document_page, mark_page_as_processed
from app.services.pdf_processing import split_pdf_into_pages
from app.services.vector_store import get_chromadb_client, store_embeddings

router = APIRouter()

@router.post("/documents/", summary="Upload and Process PDF Document", description="""
Upload a PDF document, split it into pages, generate embeddings, and store the data in a vector database.
""")
async def upload_document(file: UploadFile, db: Session = Depends(get_db)):
    """
    Upload and process a PDF document.

    Steps:
    - Validate the file type.
    - Save the uploaded file.
    - Create a document record in the database.
    - Split the PDF into pages and store them in the database.
    - Generate embeddings for the content and store them in ChromaDB.
    - Mark pages and the document as processed.
    """
    # Validate file type
    if not file.filename.endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are supported.")

    try:
        upload_dir = "./uploads" # Save the uploaded file
        os.makedirs(upload_dir, exist_ok=True)
        file_path = os.path.join(upload_dir, file.filename)

        with open(file_path, "wb") as f:
            f.write(await file.read())
        print(f"File saved at {file_path}.")

        document = create_document(db=db, title=file.filename, file_path=file_path) # Create document record in the database
        print(f"Document record created with ID: {document.id}.")

        pages = split_pdf_into_pages(file_path)  # Split PDF into pages
        if not pages:
            raise HTTPException(status_code=400, detail="Failed to extract pages from the PDF.")
        print(f"PDF split into {len(pages)} pages.")

        # Store pages in the database and mark as processed
        for page in pages: 
            stored_page = create_document_page(
                db=db,
                document_id=document.id,
                page_number=page["page_number"],
                content=page["content"],
            )
            mark_page_as_processed(db, stored_page.id)
        print(f"Pages stored and marked as processed for document ID: {document.id}.")

        # Embed content and store in ChromaDB
        client = get_chromadb_client()
        documents_to_store = [
            {"document_id": document.id, "page_number": p["page_number"], "content": p["content"]}
            for p in pages
        ]
        store_embeddings(client, collection_name="documents", documents=documents_to_store)
        print(f"Embeddings stored in ChromaDB for document ID: {document.id}.")

        # Mark the document as processed
        document.is_processed = True
        db.commit()
        print(f"Document ID: {document.id} marked as processed.")

        return {"message": "Document uploaded and processed successfully.", "document_id": document.id}

    except HTTPException as he:
        print(f"HTTP error during document processing: {he.detail}")
        raise he
    except Exception as e:
        print(f"Error processing document: {e}")
        raise HTTPException(status_code=500, detail="An unexpected error occurred while processing the document.")