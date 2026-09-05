from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models import User, Note
from app import schemas
from app.auth import get_current_user

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/notes", response_model=schemas.NoteResponse)
def create_note(
    note:schemas.NoteCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    new_note = Note(
        title = note.title,
        content = note.content,
        favourite = note.favourite,
        owner_id = current_user.id
         )

    db.add(new_note)
    db.commit()
    db.refresh(new_note)

    return new_note

@router.get("/notes", response_model=list[schemas.NoteResponse])
def get_all_notes(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    notes = db.query(Note).filter(Note.owner_id == current_user.id).all()
    return notes

@router.get("/notes/{note_id}", response_model=schemas.NoteResponse)
def get_single_note(
    note_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    note = db.query(Note).filter(Note.id == note_id).first()

    if not note:
        raise HTTPException(status_code=404, detail="Note not found")

    if note.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not Authorized")

    return note

@router.put("/notes/{note_id}", response_model=schemas.NoteResponse)
def update_note(
    note_id:int,
    updated_data:schemas.NoteUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)

):
    note = db.query(Note).filter(Note.id == note_id).first()

    if not note:
        raise HTTPException(status_code=404, detail="Note not found")

    if note.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not Authorized")

    if updated_data.title is not None:
        note.title = updated_data.title

    if updated_data.content is not None:
        note.content = updated_data.content

    if updated_data.favourite is not None:
        note.favourite = updated_data.favourite

    db.commit()
    db.refresh(note)

    return note

@router.delete("/notes/{note_id}")
def delete_note(
    note_id:int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)

):
    note = db.query(Note).filter(Note.id == note_id).first()

    if not note:
        raise HTTPException(status_code=404, detail="Note not found")

    if note.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not Authorized")

    db.delete(note)
    db.commit()

    return{"message": "Note deleted successfully "}
     