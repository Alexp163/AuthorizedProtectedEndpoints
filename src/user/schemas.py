from datetime import datetime

from pydantic import BaseModel


class UserReadSchema(BaseModel):
    id: int
    nickname: str
    data: str
    created_at: datetime
    updated_at: datetime

class UserCreateSchema(BaseModel):
    nickname: str
    data: str
    password: str


class UserUpdateSchema(BaseModel):
    nickname: str
    data: str
    password: str


class AccessTokenSchema(BaseModel):
    access_token: str
    token_type: str 
