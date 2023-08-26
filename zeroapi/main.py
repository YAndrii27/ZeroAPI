from fastapi import FastAPI

from api.v1_1 import root_router_v1_1
from api.v2_1 import root_router_v2_1

app = FastAPI()
app.include_router(root_router_v1_1)
app.include_router(root_router_v2_1)
