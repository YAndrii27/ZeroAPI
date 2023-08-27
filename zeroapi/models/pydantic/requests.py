from typing import Optional
from pydantic import BaseModel


class GetUserRequest(BaseModel):
    id: Optional[int]
    login: Optional[str]
