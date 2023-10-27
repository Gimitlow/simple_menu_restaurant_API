FROM python:3.10-slim

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apt -y update && apt -y upgrade
COPY . .

RUN apt-get -y install libpq-dev gcc \
	&& pip install --upgrade pip \
	&& pip install -Ur requirements.txt
