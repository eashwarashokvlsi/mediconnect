import json, os, time
from datetime import datetime, timezone
import boto3

sqs, s3 = boto3.client("sqs"), boto3.client("s3")
queue, bucket = os.environ["REPORT_QUEUE_URL"], os.environ["REPORT_BUCKET"]

while True:
    batch = sqs.receive_message(QueueUrl=queue, MaxNumberOfMessages=5, WaitTimeSeconds=20, VisibilityTimeout=90)
    for message in batch.get("Messages", []):
        incident = json.loads(message["Body"])
        incident["generatedAt"] = datetime.now(timezone.utc).isoformat()
        incident["disclaimer"] = "Academic demonstration only; not medical advice."
        key = f"incidents/{incident['incidentId']}.json"
        s3.put_object(Bucket=bucket, Key=key, Body=json.dumps(incident, indent=2, default=str).encode(), ContentType="application/json", ServerSideEncryption="AES256")
        sqs.delete_message(QueueUrl=queue, ReceiptHandle=message["ReceiptHandle"])
    if os.getenv("RUN_ONCE") == "true": break
    time.sleep(1)
