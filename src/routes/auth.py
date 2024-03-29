from fastapi.security import OAuth2PasswordRequestForm, HTTPAuthorizationCredentials, HTTPBearer
from src.services.auth import auth_service 
from src.database.db import  get_db
from fastapi import APIRouter, HTTPException, Depends, status, Path
from sqlalchemy.orm import Session
from sqlalchemy import text
from src.database.db import get_db
from src.schemas.auth import UserResponse, TokenModel, UserModel
from src.repository import users as repository_users

router = APIRouter(prefix='/auth', tags=["auth"])
get_refresh_token = HTTPBearer()


@router.post("/signup", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def signup(body: UserModel, db: Session = Depends(get_db)):
    exist_user = await repository_users.get_user_by_mail(body.mail, db)
    if exist_user:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT , detail="Account allready exist")
    body.password = auth_service.get_password_hash(body.password)
    new_user = await repository_users.create_user(body, db)
    return new_user


@router.post("/login", response_model = TokenModel)
async def login(body: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = await repository_users.get_user_by_mail(body.username, db)
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid email or pass")
    if not auth_service.verify_password(body.password, user.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid email or password")
    # Generate JWT
    access_token = await auth_service.create_access_token(data={"sub": user.mail, "some text":"some text!"})
    refresh_token = await auth_service.create_refresh_token(data={"sub": user.mail})
    await repository_users.update_token(user, refresh_token, db)
    return {"access_token": access_token, "refresh_token": refresh_token, "token_type": "bearer"}


@router.get('/refresh_token', response_model = TokenModel)
async def refresh_token(credentials: HTTPAuthorizationCredentials = Depends(get_refresh_token), db: Session = Depends(get_db)):
    token = credentials.credentials
    mail = await auth_service.decode_refresh_token(token)
    user = await repository_users.get_user_by_mail(mail, db)
    if user.refresh_token != token:
        await repository_users.update_token(user, None, db)
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid refresh token")

    access_token = await auth_service.create_access_token(data={"sub": mail})
    refresh_token = await auth_service.create_refresh_token(data={"sub": mail})
    await repository_users.update_token(user, refresh_token, db)
    return {"access_token": access_token, "refresh_token": refresh_token, "token_type": "bearer"}


@router.get("/")
async def root():
    return {"message": "Hello World"}

