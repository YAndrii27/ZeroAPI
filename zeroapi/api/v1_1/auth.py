from quart import Blueprint, Response
from quart_schema import validate_request
from passlib.hash import argon2
from argon2.exceptions import VerifyMismatchError
from jose import jwt
import json

from models.pydantic.requests import LoginRequest, SaveUserRequest
from config.db import session
from services.user import UserService
from config.env import SECRET

auth_blueprint = Blueprint(
    name="auth",
    import_name=__name__,
    url_prefix="/auth"
)
service = UserService(session=session)


@auth_blueprint.post("/login")
@validate_request(LoginRequest)
async def login(data: LoginRequest) -> Response:
    """Verifies auth data and returns token which can be used
    for perform futher operations"""
    user = await service.get_by_login(data.login)
    if user:
        try:
            verify: bool = argon2.verify(user.password_hash, data.password)
            if verify:
                token = jwt.encode({"login": user.login}, SECRET)
                return Response(
                    response={"message": "success"},
                    status=200,
                    headers={"Authorization": token}
                )
        except VerifyMismatchError:
            return Response(
                response={"message": "incorrect login or password"},
                status=401
            )
    return Response(
        response={"message": "user not found"},
        status=404
    )


@auth_blueprint.post("/register")
@validate_request(SaveUserRequest)
async def register(data: SaveUserRequest):
    """Check if login is aviable and if so registers user
    and returns token which can be used for perform futher operations"""
    user = await service.get_by_login(data.login)
    if not user:
        await service.save(data)
        token = jwt.encode({"login": data.login}, SECRET)
        return Response(
            response=json.dumps({"message": "success"}),
            status=201,
            headers={"Authorization": token}
        )
    return Response(
        response=json.dumps({"message": "username is already taken"}),
        status=401
    )
