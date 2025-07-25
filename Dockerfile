FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY bot.py .
# Expose 8080 for health-check
EXPOSE 8080

CMD ["python", "bot.py"]
