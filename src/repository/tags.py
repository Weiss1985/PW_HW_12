from typing import List
from sqlalchemy.sql import select
from sqlalchemy.orm import Session

from src.database.models import Tag
from src.schemas.tags import TagModel


async def get_tags(skip: int, limit: int, db: Session) -> List[Tag]:
    query = select(Tag).offset(skip).limit(limit)
    contacts = await db.execute(query)
    return contacts.scalars().all()


async def get_tag(tag_id: int, db: Session) -> Tag:
    query = select(Tag).filter_by(id=tag_id)
    contact = await db.execute(query)
    return contact.scalar_one_or_none()


async def create_tag(body: TagModel, db: Session) -> Tag:
    tag = Tag(**body.model_dump(exclude_unset=True)) 
    db.add(tag)
    await db.commit()
    await db.refresh(tag)
    return tag


async def update_tag(tag_id: int, body: TagModel, db: Session) -> Tag | None:
    query = select(Tag).filter_by(id=tag_id)
    result = await db.execute(query)
    tag = result.scalar_one_or_none()
    if tag:
        tag .name = body.name
    await db.commit()
    await db.refresh(tag)
    return tag


async def remove_tag(tag_id: int, db: Session)  -> Tag | None:
    query = select(Tag).filter_by(id=tag_id)
    tag = await db.execute(query)
    tag = tag.scalar_one_or_none()
    if tag:
        await db.delete(tag)
        await db.commit()
    return tag
