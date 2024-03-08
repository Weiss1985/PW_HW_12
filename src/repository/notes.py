from typing import List

from sqlalchemy.orm import Session
from sqlalchemy.sql import select

from src.database.models import Note, Tag
from src.schemas.notes import NoteModel, NoteUpdate, NoteStatusUpdate


async def get_notes(skip: int, limit: int, db: Session) -> List[Note]:
    query = select(Note).offset(skip).limit(limit)
    contacts = await db.execute(query)
    return contacts.scalars().all()


async def get_note(note_id: int, db: Session) -> Note:
    query = select(Note).filter_by(id=note_id)
    contact = await db.execute(query)
    return contact.scalar_one_or_none()


async def create_note(body: NoteModel, db: Session) -> Note|None:
    note = Note(**body.model_dump(exclude_unset=True)) 
    db.add(note)
    await db.commit()
    # await db.refresh(note)
    return note


async def remove_note(note_id: int, db: Session) -> Note | None:
    query = select(Note).filter_by(id=note_id)
    note = await db.execute(query)
    note = note.scalar_one_or_none()
    if note:
        await db.delete(note)
        await db.commit()
    return note


async def update_note(note_id: int, body: NoteUpdate, db: Session) -> Note | None:
    query = select(Note).filter_by(id=note_id)
    result = await db.execute(query)
    note = result.scalar_one_or_none()
    if note:
        stmt = select([Tag]).where(Tag.id.in_(body.tags))
        tags = db.execute(stmt).fetchall()
        note.title = body.title
        note.description = body.description
        note.done = body.done
        note.tags = tags
        await db.commit()
        await db.refresh(note)
    return note


async def update_status_note(note_id: int, body: NoteStatusUpdate, db: Session) -> Note | None:
    query = select(Note).filter_by(id=note_id)
    result = await db.execute(query)
    note = result.scalar_one_or_none()
    if note:
        note.done = body.done
        await db.commit()
        await db.refresh(note)
    return note
