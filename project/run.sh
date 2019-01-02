#!/bin/bash

rm -rf celerybeat* &
celery worker -A server.worker.celery --loglevel=info &
celery beat -A server.worker.celery --loglevel=info &
gunicorn -w 1 -b 0.0.0.0:8080 --log-level=info --reload server.wsgi
