
import os
from server.extensions.celery import create_celery
from server.app import create_app

application = create_app(os.getenv("FLASK_CONFIG") or "default")
application.app_context().push()

celery = create_celery(application)

from server.extensions.celery import tasks
tasks.setup()