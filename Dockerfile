FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY bot.py .
# Expose for clarity, though Cloud Run doesn’t require it
EXPOSE 8080

CMD ["python", "bot.py"]
