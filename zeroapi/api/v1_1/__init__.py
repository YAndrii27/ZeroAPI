from fastapi import APIRouter

from .users import user_router
from .notes import note_router
from .auth import auth_router


root_router_v1_1 = APIRouter(prefix="/v1.1")
root_router_v1_1.include_router(user_router)
root_router_v1_1.include_router(note_router)
root_router_v1_1.include_router(auth_router)
