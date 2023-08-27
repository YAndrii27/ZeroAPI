from fastapi import FastAPI

from config.db import init_db
from config import env

from api.v1_1 import root_router_v1_1
from api.v2_1 import root_router_v2_1

app = FastAPI(on_startup=[init_db])
app.include_router(root_router_v1_1)
app.include_router(root_router_v2_1)
