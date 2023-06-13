FROM python:3.11.1-alpine
RUN mkdir /app
WORKDIR /app
COPY src/ .
COPY requirements.txt .
RUN pip install -U pip --no-cache-dir
RUN	pip install -r /app/requirements.txt --no-cache-dir
CMD ["python", "application.py"]

