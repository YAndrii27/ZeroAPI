from quart import Blueprint

from .users import user_blueprint
from .notes import note_blueprint
from .auth import auth_blueprint

root_blueprint_v2_1 = Blueprint(
    name="v2_1",
    import_name=__name__,
    url_prefix="/v2.1"
)
root_blueprint_v2_1.register_blueprint(auth_blueprint)
root_blueprint_v2_1.register_blueprint(note_blueprint)
root_blueprint_v2_1.register_blueprint(user_blueprint)
