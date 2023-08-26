from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import BaseModel
from .users import UserModel


class NoteModel(BaseModel):
    __tablename__ = "notes"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column()
    text: Mapped[str] = mapped_column()
    owner: Mapped["UserModel"] = relationship(back_populates="note")
