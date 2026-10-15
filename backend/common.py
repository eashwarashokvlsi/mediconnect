import json
import os
from decimal import Decimal

THRESHOLDS = {"heartRate": (50, 120), "spo2": (94, 100), "temperature": (35.0, 38.0)}

def classify(reading):
    breaches = []
    for key, (low, high) in THRESHOLDS.items():
        value = float(reading[key])
        if value < low or value > high:
            breaches.append({"metric": key, "value": value, "expected": [low, high]})
    return {"status": "ABNORMAL" if breaches else "NORMAL", "breaches": breaches}

def response(code, body):
    return {"statusCode": code, "headers": {"content-type": "application/json", "access-control-allow-origin": os.getenv("APP_ORIGIN", "*")}, "body": json.dumps(body, default=lambda x: float(x) if isinstance(x, Decimal) else str(x))}

