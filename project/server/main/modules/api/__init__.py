from flask import Blueprint
from flask_restplus import Api, abort

api_v1 = Api(
    title="GDN Infrastructure Manager DNS API",
    version="0.1.2"
)

from .http_exceptions import *
from .util import *
from .decorators import *

def init_app(app, **kwargs):
    blueprint = Blueprint("api", __name__, url_prefix="/api/v1")

    from . import routes
    routes.setup(api_v1)

    api_v1.init_app(blueprint)
    app.register_blueprint(blueprint)