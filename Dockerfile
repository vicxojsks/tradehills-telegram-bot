FROM python:3.11-slim

WORKDIR /app
COPY . /app

RUN pip install --no-cache-dir -r requirements.txt

# Use Gunicorn to serve the Flask app in bot.py on the PORT Cloud Run provides
CMD ["gunicorn", "--bind", "0.0.0.0:$PORT", "bot:app"]
