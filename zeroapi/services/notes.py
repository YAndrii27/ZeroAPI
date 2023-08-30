from typing import Sequence

from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession
from sqlalchemy.future import select

from models.database.notes import NoteModel
from models.database.users import UserModel
from models.pydantic.requests import SaveNoteRequest


class NoteService:
    def __init__(self, session: async_sessionmaker[AsyncSession]) -> None:
        self._session = session

    async def get_by_owner(
            self,
            owner_id: int | None = None,
            owner_login: int | None = None,
            count: int | None = 0
    ) -> Sequence[NoteModel] | NoteModel | None:
        """Returns all notes which has user with
        correspond login or ID. One of optional params
        is required

        @param owner_id: int | None - user ID
        @param owner_login: int | None - user login
        @param count: int | None - number of notes to return. If equals 0
        returns all rows

        @returns Sequence[NoteModel] | None - list of NoteModel's or None if
        user has no notes

        @throws TypeError in case neither owner ID or owner login was given"""
        async with self._session() as session:
            async with session.begin():
                if owner_login:
                    query = await session.scalars(
                        select(UserModel).where(UserModel.login == owner_login)
                    )
                elif owner_id:
                    query = await session.scalars(
                        select(UserModel).where(UserModel.id == owner_id)
                    )
                else:
                    raise TypeError("Owner ID or Owner login is required")
                owner = query.one_or_none()
                if owner:
                    query = await session.scalars(
                        select(NoteModel).where(NoteModel.owner == owner)
                    )
                    if count == 0:
                        return query.all()
                    elif count == 1:
                        return query.first()
                    return query.fetchmany(size=count)
        return

    async def get_one_by_id(self, id: int) -> NoteModel | None:
        """Returns note which has correspond ID

        @param id: int | None - note ID

        @returns NoteModel | None - NoteModel or None if note doesn't exist"""
        async with self._session() as session:
            async with session.begin():
                query = await session.scalars(
                    select(NoteModel).where(NoteModel.id == id)
                )
                note: NoteModel | None = query.one_or_none()
                return note

    async def save(
            self,
            note: NoteModel | SaveNoteRequest | None = None,
            **kwargs
    ):
        """Saves note which is in form of SQLAlchemy model
        or given as correspond params

        @param note: NoteModel | None - SQLAlchemy note's model
        @param **kwargs - kwargs which contain title, text and owner
        of the note

        @returns bool - True if note was saved correct"""
        if isinstance(note, SaveNoteRequest):
            note = NoteModel(**note.dict())
        async with self._session() as session:
            async with session.begin():
                if note:
                    session.add(note)
                else:
                    session.add(NoteModel(
                        title=kwargs.get("title"),
                        text=kwargs.get("text"),
                        owner=kwargs.get("owner")
                    ))
                await session.commit()
                return True
