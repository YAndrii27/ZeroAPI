from typing import Optional
from pydantic import BaseModel

from enums.roles import Roles
from models.database.users import UserModel


class GetUserRequest(BaseModel):
    id: Optional[int] = None
    login: Optional[str] = None


class GetNotesRequest(BaseModel):
    note_id: Optional[int] = None
    owner_id: Optional[int] = None
    owner_login: Optional[int] = None


class SaveUserRequest(BaseModel):
    id: Optional[int] = None
    login: Optional[str] = None
    password_hash: Optional[str] = None
    role: Optional[Roles] = None


class SaveNoteRequest(BaseModel):
    id: Optional[int] = None
    title: Optional[str] = None
    text: Optional[str] = None
    owner: Optional[UserModel] = None


class LoginRequest(BaseModel):
    login: str
    password: str
