FROM python:3.11-slim

ARG APP_PORT

ENV APP_PORT=${APP_PORT}\
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1
WORKDIR /backend

COPY requirements.txt .

RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE ${APP_PORT}

ENTRYPOINT ["python3"]
CMD ["app/main.py"]
