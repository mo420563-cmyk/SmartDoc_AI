from fastapi import APIRouter, File, HTTPException, UploadFile, status
from sqlalchemy.orm import Session

from database import engine
from models import Document
from schemas import DocumentCreate, DocumentResponse

router = APIRouter(prefix="/documents", tags=["documents"])


@router.get("", response_model=list[DocumentResponse], summary="List all documents")
def list_documents():
    with Session(engine) as db:
        return db.query(Document).all()


@router.post("", response_model=DocumentResponse, status_code=status.HTTP_201_CREATED, summary="Create a document")
def create_document(document_data: DocumentCreate):
    with Session(engine) as db:
        document = Document(**document_data.model_dump())
        db.add(document)
        db.commit()
        db.refresh(document)
        return document


@router.get("/{document_id}", response_model=DocumentResponse, summary="Get one document", responses={404: {"description": "Document not found"}})
def get_document(document_id: int):
    with Session(engine) as db:
        document = db.get(Document, document_id)
        if document is None:
            raise HTTPException(status_code=404, detail="Document not found")
        return document


@router.put("/{document_id}", response_model=DocumentResponse, summary="Update a document", responses={404: {"description": "Document not found"}})
def update_document(document_id: int, document_data: DocumentCreate):
    with Session(engine) as db:
        document = db.get(Document, document_id)
        if document is None:
            raise HTTPException(status_code=404, detail="Document not found")

        for key, value in document_data.model_dump().items():
            setattr(document, key, value)

        db.commit()
        db.refresh(document)
        return document


@router.delete("/{document_id}", summary="Delete a document", responses={404: {"description": "Document not found"}})
def delete_document(document_id: int):
    with Session(engine) as db:
        document = db.get(Document, document_id)
        if document is None:
            raise HTTPException(status_code=404, detail="Document not found")

        db.delete(document)
        db.commit()
        return {"message": "Document deleted successfully"}


@router.post("/upload", response_model=DocumentResponse, status_code=status.HTTP_201_CREATED, summary="Upload a text document")
async def upload_document(file: UploadFile = File(...)):
    if file.content_type != "text/plain":
        raise HTTPException(status_code=400, detail="Only text/plain uploads are supported")

    raw_content = await file.read()
    try:
        content = raw_content.decode("utf-8")
    except UnicodeDecodeError:
        raise HTTPException(status_code=400, detail="Uploaded text file must be UTF-8 encoded")

    title = file.filename or "Uploaded document"
    with Session(engine) as db:
        document = Document(title=title[:120], content=content, priority=1)
        db.add(document)
        db.commit()
        db.refresh(document)
        return document
