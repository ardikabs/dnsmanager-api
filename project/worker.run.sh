#!/bin/bash

celery beat -A server.worker.celery --loglevel=info &
celery worker -A server.worker.celery --loglevel=info