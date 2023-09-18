from typing import Optional
from pydantic import BaseModel

from enums.roles import Roles


class UserModel(BaseModel):
    id: int
    login: Optional[str] = None
    password_hash: Optional[str] = None
    role: Optional[Roles] = None
