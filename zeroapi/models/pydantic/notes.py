from typing import Optional
from pydantic import BaseModel

from .users import UserModel


class NoteModel(BaseModel):
    id: int
    title: Optional[str] = None
    text: Optional[str] = None
    owner: Optional[UserModel] = None
