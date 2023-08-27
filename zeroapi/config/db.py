from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from models.database.base import BaseModel
from .env import PGUSER, PGHOST, PGPORT, PGDATABASE

engine = create_async_engine(
    F"postgresql+asyncpg://{PGUSER}@{PGHOST}:{PGPORT}/{PGDATABASE}"
)
session = async_sessionmaker(engine)


async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(BaseModel.metadata.create_all)
