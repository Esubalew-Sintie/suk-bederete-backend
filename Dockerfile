
FROM python:3.12.3-slim

ENV PYTHONUNBUFFERED 1

WORKDIR /app

COPY requirements.txt .

RUN python -m pip install -r requirements.txt

COPY . /app/

RUN chmod +x /app/django.sh

EXPOSE 8000

ENTRYPOINT ["/app/django.sh"]