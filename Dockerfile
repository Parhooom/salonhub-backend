FROM python:3.10.7-alpine3.16

RUN addgroup app && adduser -S -G app app
USER app

ENV PIP_DISABLE_PIP_VERSION_CHECK=1
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY requirements/requirements.txt .
RUN pip install -r requirements.txt

COPY . .