import logging

from quart import Quart
from quart_schema import QuartSchema

from config.db import init_db
from config import env
from middlewares.auth import AuthMiddleware

from api.v1_1 import root_blueprint_v1_1
from api.v2_1 import root_blueprint_v2_1

logger = logging.basicConfig(level="WARNING")

app = Quart("Zero API")
schema = QuartSchema(app=app)
app.startup = init_db

app.register_blueprint(root_blueprint_v1_1)
app.register_blueprint(root_blueprint_v2_1)

app.asgi_app = AuthMiddleware(app=app.asgi_app)
