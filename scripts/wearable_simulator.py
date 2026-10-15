import argparse, json, random, ssl, time, uuid
from urllib import request

def reading(patient_id, abnormal=False):
    return {"patientId":patient_id,"readingId":str(uuid.uuid4()),"recordedAt":int(time.time()),"heartRate":145 if abnormal else random.randint(68,88),"spo2":90 if abnormal else random.randint(96,99),"temperature":round(random.uniform(36.4,37.2),1)}

if __name__ == "__main__":
    p=argparse.ArgumentParser(description="Generate synthetic MediConnect readings")
    p.add_argument("--patient",default="demo-patient"); p.add_argument("--endpoint",help="Optional HTTP ingestion endpoint"); p.add_argument("--count",type=int,default=10); p.add_argument("--abnormal-every",type=int,default=0)
    a=p.parse_args()
    for i in range(a.count):
        body=reading(a.patient, bool(a.abnormal_every and (i+1)%a.abnormal_every==0)); print(json.dumps(body))
        if a.endpoint: request.urlopen(request.Request(a.endpoint,data=json.dumps(body).encode(),headers={"content-type":"application/json"}),context=ssl.create_default_context()).read()
        time.sleep(1)
