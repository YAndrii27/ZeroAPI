from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession
from sqlalchemy.future import select

from models.database.users import UserModel
from models.pydantic.requests import SaveUserRequest


class UserService:
    def __init__(self, session: async_sessionmaker[AsyncSession]) -> None:
        self._session = session

    async def get_by_id(self, id: int) -> UserModel | None:
        async with self._session() as session:
            async with session.begin():
                query = await session.scalars(
                    select(UserModel).where(UserModel.id == id)
                )
                user = query.one_or_none()
                return user

    async def get_by_login(self, login: str) -> UserModel | None:
        async with self._session() as session:
            async with session.begin():
                query = await session.scalars(
                    select(UserModel).where(UserModel.login == login)
                )
                user = query.one_or_none()
                return user

    async def save(
            self,
            user: UserModel | SaveUserRequest | None = None,
            **kwargs
    ):
        if isinstance(user, SaveUserRequest):
            user = UserModel(**user.dict())
        async with self._session() as session:
            async with session.begin():
                if user:
                    session.add(user)
                else:
                    session.add(UserModel(
                        login=kwargs.get("login"),
                        password_hash=kwargs.get("password_hash"),
                        owner=kwargs.get("owner"),
                        role=kwargs.get("role")
                    ))
                await session.commit()
                return True
