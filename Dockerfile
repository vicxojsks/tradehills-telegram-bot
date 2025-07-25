FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY bot.py .

# Use shell form so $PORT is expanded at runtime
CMD exec gunicorn --bind 0.0.0.0:$PORT bot:app
