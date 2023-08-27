from fastapi import APIRouter, HTTPException
import json

from services.user import UserService
from config.db import session
from models.pydantic.requests import GetUserRequest

user_router = APIRouter(prefix="/user")
service = UserService(session=session)


@user_router.post("/")
async def get_user(request: GetUserRequest):
    if request.id:
        user = await service.get_by_id(id=request.id)
    elif request.login:
        user = await service.get_by_login(login=request.login)
    else:
        raise HTTPException(
            status_code=400,
            detail="User ID or Login is required"
        )
    if user:
        return json.dumps(user.__dict__)
    return {"message": "user not found"}
