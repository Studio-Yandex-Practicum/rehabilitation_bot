FROM python:3.11.1-alpine

WORKDIR /app/src

COPY requirements.txt .

RUN pip3 install -r requirements.txt --no-cache-dir

COPY / /app

CMD ["python", "application.py"]