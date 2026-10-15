import json
import os
import boto3
from common import response

rds = boto3.client("rds-data")

def handler(event, _context):
    route = event.get("routeKey", "")
    claims = event.get("requestContext", {}).get("authorizer", {}).get("jwt", {}).get("claims", {})
    user_id = claims.get("sub", "demo-user")
    if route == "GET /health":
        return response(200, {"service": "mediconnect-api", "status": "ok"})
    if route == "GET /appointments":
        _ensure_schema()
        result = _sql("SELECT id, doctor_name, starts_at, status FROM appointments WHERE patient_id=:patient ORDER BY starts_at", [{"name":"patient","value":{"stringValue":user_id}}])
        return response(200, {"appointments": result.get("records", [])})
    if route == "POST /appointments":
        _ensure_schema()
        body = json.loads(event.get("body") or "{}")
        if not body.get("doctorName") or not body.get("startsAt"):
            return response(400, {"message": "doctorName and startsAt are required"})
        _sql("INSERT INTO appointments(patient_id,doctor_name,starts_at,status) VALUES(:patient,:doctor,:starts,'CONFIRMED')", [
            {"name":"patient","value":{"stringValue":user_id}}, {"name":"doctor","value":{"stringValue":body["doctorName"]}}, {"name":"starts","value":{"stringValue":body["startsAt"]}}])
        return response(201, {"status": "CONFIRMED"})
    return response(404, {"message": "Route not found"})

def _sql(sql, parameters=None):
    return rds.execute_statement(resourceArn=os.environ["DB_CLUSTER_ARN"], secretArn=os.environ["DB_SECRET_ARN"], database="mediconnect", sql=sql, parameters=parameters or [])

def _ensure_schema():
    _sql("CREATE TABLE IF NOT EXISTS appointments (id BIGSERIAL PRIMARY KEY, patient_id VARCHAR(64) NOT NULL, doctor_name VARCHAR(120) NOT NULL, starts_at TIMESTAMPTZ NOT NULL, status VARCHAR(24) NOT NULL DEFAULT 'CONFIRMED', created_at TIMESTAMPTZ NOT NULL DEFAULT NOW())")

