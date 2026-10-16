# MediConnect deployment proof

AWS account: `670099380958`  
Primary region: `ap-south-1` (Mumbai)  
Comprehend Medical region: `ap-southeast-2` (Sydney)  
Budget alert: USD 15 monthly  
Data classification: synthetic academic demonstration only

## Verification state

- Local frontend production build: passed
- Backend classifier unit tests: 2/2 passed
- CloudFormation template syntax and AWS validation: passed
- GitHub repository: public and source pushed
- AWS stack `mediconnect-dev-v4`: `CREATE_COMPLETE`
- Public frontend upload: 3/3 objects succeeded
- Public frontend: verified live
- API `/prod/health`: verified `status: ok`
- Aurora PostgreSQL Express `mediconnect-express`: available (0–4 ACUs, five-minute auto-pause)

## Live endpoints

- <http://mediconnect-dev-v4-frontendbucket-e7nhk2ftv3wi.s3-website.ap-south-1.amazonaws.com>
- <https://9w5sd7nqil.execute-api.ap-south-1.amazonaws.com/prod/health>

## Screenshot index

- `cloudformation/`: successful stack resources and outputs
- `cognito/`: deployed user pool
- `api-gateway/`: HTTP API and live health response
- `lambda/`: appointment API function
- `rds/`: Aurora Express creation and available state
- `iot-core/`: rules engine
- `dynamodb/`: vitals table
- `sns/` and `sqs/`: alerts and report queues
- `s3/`: uploaded frontend objects
- `ecs/` and `ecr/`: Fargate cluster and worker repository
- `cloudwatch/`: alarms
- `budget/`: USD 15 monthly cap
- `frontend/`: local and live dashboards

## Honest limitations

- Kinesis is not deployed because this AWS account returned a service-subscription requirement. The active IoT-to-Lambda fallback is reflected in the stack and repository.
- The ECR repository and Fargate task definition are deployed, but no continuously running task is kept active to protect the USD 15 cap.
- SNS email delivery remains pending until the recipient confirms the AWS subscription email.

Screenshots are organized by service as deployment completes. A screenshot is proof of observed console state only; stack resource status and endpoint tests are the correctness checks.
