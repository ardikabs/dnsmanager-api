
from flask_restplus import Namespace

api = Namespace("records", description="DNS Records Related Operation")

from . import resource