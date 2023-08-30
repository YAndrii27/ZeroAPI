from fastapi import APIRouter, Response
from passlib.hash import argon2
from argon2.exceptions import VerifyMismatchError
from jose import jwt
import json

from models.pydantic.requests import LoginRequest, SaveUserRequest
from config.db import session
from services.user import UserService
from config.env import SECRET

auth_router = APIRouter(prefix="/auth")
service = UserService(session=session)


@auth_router.post("/login")
async def login(request: LoginRequest):
    user = await service.get_by_login(request.login)
    if user:
        try:
            verify: bool = argon2.verify(user.password_hash, request.password)
            if verify:
                token = jwt.encode({"login": user.login}, SECRET)
                return Response(
                    content=json.dumps({"message": "success"}),
                    headers={"Authentification": token}
                )
        except VerifyMismatchError:
            return Response(
                content=json.dumps({"message": "incorrect login or password"}),
                status_code=401
            )


@auth_router.post("/register")
async def register(request: SaveUserRequest):
    user = await service.get_by_login(request.login)
    if not user:
        await service.save(request)
        token = jwt.encode({"login": request.login}, SECRET)
        return Response(
            content=json.dumps({"message": "success"}),
            status_code=201,
            headers={"Authentification": token}
        )
    return Response(
        content=json.dumps({"message": "username already used"}),
        status_code=401
    )
