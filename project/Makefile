.PHONY: clean system-packages python-packages install tests dev-run server-run worker-run dev-setup prod-setup worker-setup

clean:
		find . -type f -name '*.pyc' -delete
		find . -type f -name '*.log' -delete

system-packages:
		sudo apt install python-pip -y

python-packages:
		pip install -r requirements.txt

install: system-packages python-packages

tests:
		python manage.py test

dev-run:
		python manage.py run

server-run:
		gunicorn -w 1 -b 0.0.0.0:8080 --log-level=debug --reload server.wsgi

worker-run:
		celery worker -A server.worker.worker --loglevel=info

dev-setup: clean install tests dev-run
prod-setup: clean install tests server-run
worker-setup: clean install tests worker-run