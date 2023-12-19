FROM python:3.11

RUN python -m pip install --upgrade pip

COPY requirements.txt .
RUN python -m pip install -r requirements.txt

COPY secret_santa .
COPY db.sqlite3 .

EXPOSE 8080

CMD python -m uvicorn --host 0.0.0.0 --port 8080 secret_santa.asgi:application
