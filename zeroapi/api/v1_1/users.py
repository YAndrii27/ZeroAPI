from fastapi import APIRouter, HTTPException, Response
import json

from services.user import UserService
from config.db import session
from models.pydantic.requests import GetUserRequest, SaveUserRequest

user_router = APIRouter(prefix="/user")
service = UserService(session=session)


@user_router.post("/get", tags=["users"], deprecated=True)
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
    return Response(
        content=json.dumps({"message": "user not found"}),
        status_code=400
    )


@user_router.post("/save", tags=["users"], deprecated=True)
async def save_user(request: SaveUserRequest):
    await service.save(request)
    return Response(
        content=json.dumps({"message": "success"}),
        status_code=201
    )
