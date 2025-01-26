FROM python:3.11.11-slim

WORKDIR /app

COPY requirements.txt .
COPY Text.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 80

CMD ["fastapi", "run", "main.py", "--port", "80"]