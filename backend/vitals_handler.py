import base64, json, os, time, uuid
from decimal import Decimal
import boto3
from common import classify

ddb = boto3.resource("dynamodb")
sns = boto3.client("sns")
sqs = boto3.client("sqs")
medical = boto3.client("comprehendmedical", region_name=os.getenv("MEDICAL_REGION", "ap-southeast-2"))

def handler(event, _context):
    table = ddb.Table(os.environ["VITALS_TABLE"])
    processed = 0
    for record in event.get("Records", []):
        payload = json.loads(base64.b64decode(record["kinesis"]["data"]))
        verdict = classify(payload)
        item = {**payload, "patientId": payload.get("patientId", "demo-patient"), "readingId": payload.get("readingId", str(uuid.uuid4())), "recordedAt": int(payload.get("recordedAt", time.time())), "status": verdict["status"], "ttl": int(time.time()) + 7776000}
        table.put_item(Item=json.loads(json.dumps(item), parse_float=Decimal))
        if verdict["status"] == "ABNORMAL":
            entities = []
            if payload.get("clinicalNote"):
                entities = medical.detect_entities_v2(Text=payload["clinicalNote"][:20000]).get("Entities", [])
            incident = {"incidentId": str(uuid.uuid4()), "reading": item, "breaches": verdict["breaches"], "medicalEntities": entities}
            sns.publish(TopicArn=os.environ["ALERT_TOPIC_ARN"], Subject="MediConnect abnormal vital alert", Message=json.dumps(incident, default=str))
            sqs.send_message(QueueUrl=os.environ["REPORT_QUEUE_URL"], MessageBody=json.dumps(incident, default=str))
        processed += 1
    return {"processed": processed}

