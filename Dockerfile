FROM python:3.6.5-slim

ADD project/ /project

WORKDIR /project

RUN pip install -r requirements.txt

EXPOSE 8080/tcp

CMD ["/bin/bash","run.sh"]