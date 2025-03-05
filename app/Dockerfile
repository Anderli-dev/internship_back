FROM python:3.11-slim

ARG APP_PORT

WORKDIR /

COPY requirements.txt .

RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE ${APP_PORT}

WORKDIR /app

ENTRYPOINT ["python3"]
CMD ["main.py"]
