FROM python:3.12-slim
WORKDIR /app
COPY worker.py .
RUN pip install --no-cache-dir boto3
CMD ["python", "worker.py"]
