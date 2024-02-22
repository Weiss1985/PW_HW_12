from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, Field, EmailStr, PastDate


class UserModel(BaseModel):
    username: str = Field(max_length=50, min_length=3)
    mail: EmailStr = Field(max_length=60, min_length=6)
    password: str = Field(min_length=4, max_length=300)


class UserResponse(UserModel):
    id: int
    username: str
    mail: str  
    avatar: str 
    created_at: datetime

    class Config:
        from_attributes = True


class UsertUpdate(UserModel):
    first_name: str  
    second_name: str 
    mail: EmailStr  
    birthday: PastDate 
    addition: str 
    created_at: datetime

    
class TokenModel(BaseModel):
    acses_token: str 
    refresh_token: str 
    token_type: str = "bearer"








