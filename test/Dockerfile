FROM python:3.10-slim

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apt -y update && apt -y upgrade
COPY . .

RUN pip install --upgrade pip \
	&& pip install -Ur requirements.txt

CMD ["pytest", "test.py"]
