from envparse import env
from pathlib import Path


dotenv_path = Path(__file__).parent.parent.parent/".env"
env.read_envfile(path=dotenv_path)

PGUSER = env.str("PGUSER")
PGHOST = env.str("PGHOST")
PGPORT = env.int("PGPORT")
PGDATABASE = env.str("PGDATABASE")

SECRET = env.str("SECRET")
