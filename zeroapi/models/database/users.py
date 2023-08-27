from sqlalchemy.orm import Mapped, mapped_column

from .base import BaseModel
from enums.roles import Roles


class UserModel(BaseModel):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    login: Mapped[str] = mapped_column(unique=True)
    password_hash: Mapped[str] = mapped_column()
    role: Mapped[Roles] = mapped_column()
