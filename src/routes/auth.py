from fastapi.security import OAuth2PasswordRequestForm
from src.services.auth import create_access_token, get_current_user, Hash
from src.database.db import  get_db
from src.database.models import User
from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session
from sqlalchemy import text
from src.database.db import get_db
from src.schemas.auth import UserResponse, UsertUpdate, UserModel
from src.repository import contacts as repository_contacts

router = APIRouter(prefix='/auth', tags=["auth"])

hash_handler = Hash()

@router.post("/signup")
async def signup(body: UserModel, db: Session = Depends(get_db)):
    return {"new_user": 1}


@router.post("/login")
async def login(body: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    return {"access_token": "access_token", "token_type": "bearer"}


@router.get("/")
async def root():
    return {"message": "Hello World"}

