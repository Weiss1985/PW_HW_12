from typing import List
from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session
from sqlalchemy import text
from src.database.db import get_db
from src.schemas.contacts import ContactModel, ContactResponse, ContactUpdate
from src.repository import contacts as repository_contacts

router = APIRouter(prefix='/contacts', tags=["contacts"])


@router.get("/", response_model=List[ContactResponse] | None)
async def read_contacts(contacts_find_days: int = 0, contacts_find_data: str = "0", skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    if contacts_find_data != "0":
        contacts = await repository_contacts.find_contacts(contacts_find_data, db)
        if contacts:                    
            return contacts
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No Contact with {contacts_find_data}")
    if contacts_find_days != 0:
        contacts = await repository_contacts.find_contacts_delta_time (contacts_find_days, db)
        if contacts:                    
            return contacts
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No birthdays in {contacts_find_days} days")
    contacts = await repository_contacts.get_contacts(skip, limit, db)
    if contacts:
        return contacts
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Contact not found")


@router.get("/{contact_id}", response_model=ContactResponse)
async def read_contact(contact_id: int = 1, db: Session = Depends(get_db)):
    contact = await repository_contacts.get_contact(contact_id, db)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Contact not found")
    return contact


@router.post("/", response_model=ContactResponse)
async def create_contact(body: ContactModel, db: Session = Depends(get_db)):
    try:
        return await repository_contacts.create_contact(body, db)
    except Exception as err:
        print(err)
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="not valid data")


@router.put("/{contact_id}", response_model=ContactResponse, status_code=status.HTTP_201_CREATED)
async def update_contact(body: ContactUpdate, contact_id: int, db: Session = Depends(get_db)):
    contact = await repository_contacts.update_contact(contact_id, body, db)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Contact not found")
    return contact


@router.delete("/{contact_id}", response_model=ContactResponse)
async def remove_contact(contact_id: int, db: Session = Depends(get_db)):
    contact = await repository_contacts.remove_contact(contact_id, db)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Contact not found")
    return contact



