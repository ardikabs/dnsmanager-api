
import os
from server import make_server

application = make_server(os.getenv("FLASK_CONFIG") or "default", gunicorn=True)