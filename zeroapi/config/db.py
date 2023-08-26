from os import getenv
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

PGUSER = getenv("PGUSER", "")
PGHOST = getenv("PGHOST", "")
PGPORT = getenv("PGPORT", "")
PGDATABASE = getenv("PGDATABASE", "")

engine = create_async_engine(
    F"postgresql://{PGUSER}@{PGHOST}:{PGPORT}/{PGDATABASE}"
)
session = async_sessionmaker(engine)
