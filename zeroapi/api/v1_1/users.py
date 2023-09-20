from quart import Blueprint, Response
from quart_schema import validate_request

from services.user import UserService
from config.db import session
from models.pydantic.requests import GetUserRequest, SaveUserRequest

user_blueprint = Blueprint(
    name="user",
    import_name=__name__,
    url_prefix="/user"
)
service = UserService(session=session)


@user_blueprint.post("/get")
@validate_request(GetUserRequest)
async def get_user(request: GetUserRequest):
    """Get user by their ID or login. One of two field is required"""
    if request.id:
        user = await service.get_by_id(id=request.id)
    elif request.login:
        user = await service.get_by_login(login=request.login)
    else:
        return Response(
            status=400,
            response={"message": "User ID or Login is required"}
        )
    if user:
        return Response(
            response=user.__dict__,
            status=200
        )
    return Response(
        response={"message": "user not found"},
        status=400
    )


@user_blueprint.post("/save")
@validate_request(SaveUserRequest)
async def save_user(request: SaveUserRequest):
    """Updates/Creates user data"""
    await service.save(request)
    return Response(
        response={"message": "success"},
        status=201
    )
