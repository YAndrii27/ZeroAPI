from typing import Any
from hypercorn.typing import Scope, ASGIReceiveCallable, ASGISendCallable
from quart import Quart, Response
from jose import jwt
from jose.exceptions import JWTError, JWTClaimsError, ExpiredSignatureError

from config.env import SECRET


class AuthMiddleware:
    def __init__(self, app: Quart) -> None:
        self.app = app

    async def __call__(
            self,
            scope: Scope,
            receive: ASGIReceiveCallable,
            send: ASGISendCallable
    ) -> Any:
        if (
            b"auth" in scope["raw_path"] or
                scope["raw_path"] in [b"/docs", b"/openapi.json"]):
            return await self.app(
                scope=scope,
                receive=receive,
                send=send
            )
        for header, value in scope['headers']:
            if header == b"Authorization":
                try:
                    token = header.split(" ")[1]
                    jwt.decode(token=token, key=SECRET)
                    response = await self.app(
                        scope=scope,
                        receive=receive,
                        send=send
                    )
                    return response
                except IndexError:
                    raise Response(
                        status=401,
                        response={"message": "incorrect Authorization header"}
                    )
                except ExpiredSignatureError:
                    raise Response(
                        status=401,
                        response={
                            "message": "expired token, please re-login again"
                        })
                except (JWTClaimsError, JWTError):
                    raise Response(
                        status=401,
                        response={"message": "incorrect token"}
                    )
