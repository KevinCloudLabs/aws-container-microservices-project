FROM python:3.12-slim

WORKDIR /app

COPY . .

RUN pip install flask boto3 flask-cors

CMD ["python", "app.py"]