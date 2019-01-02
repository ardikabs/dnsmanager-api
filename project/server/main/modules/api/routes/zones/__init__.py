
from flask_restplus import Namespace

api = Namespace("zones", description="DNS Zones Related Operation")

from . import resource