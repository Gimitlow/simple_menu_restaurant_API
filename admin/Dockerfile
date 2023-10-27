FROM python:3.10-slim

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY . ./project
WORKDIR ./project 

ENV PATH="/opt/venv/bin:$PATH"

RUN apt -y update && apt -y upgrade

RUN pip install --upgrade pip \
	&& pip install -Ur requirements.txt
