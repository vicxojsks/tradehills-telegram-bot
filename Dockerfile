FROM python:3.11-slim

WORKDIR /app
COPY . /app

RUN pip install --no-cache-dir -r requirements.txt

# instead of exec-form, use shell form so $PORT is interpolated
CMD gunicorn --bind 0.0.0.0:$PORT bot:app

