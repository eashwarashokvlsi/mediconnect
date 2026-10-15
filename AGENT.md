# MediConnect Continuation Handoff

This file is the live handoff for any agent continuing the project. Update the **Current status** and **Checkpoint log** after every material change. Never place AWS credentials, GitHub tokens, passwords, or patient data here.

## Mission and constraints

- Build and publicly deliver the MediConnect academic project described by `D:\AWS (1).pdf`.
- GitHub repository: <https://github.com/eashwarashokvlsi/mediconnect>
- AWS account: `670099380958` (`eashwarashokvlsi`), region `ap-south-1` (Mumbai).
- Use synthetic/demo health data only.
- Authorized monthly budget cap: USD 15; alert email: `eashwarashokvlsi@gmail.com`.
- Store user-facing proof under `C:\Users\eashw\Documents\Codex\2026-10-15\d\outputs\mediconnect-deployment-proof`.
- Do not delete failed CloudFormation stacks or other cloud resources without action-time confirmation.
- Comprehend Medical is not offered in Mumbai. The template calls it in `ap-southeast-2` (Sydney), the nearest supported region.

## Current status

Last updated: 2026-10-16 00:10 IST

- Application code, infrastructure, README, license, tests, and worker are in this repository and pushed to `main`.
- Unit tests: 2/2 passed. Vite production build passed.
- Repository is public and its description is set.
- Local dashboard proof exists at `outputs/mediconnect-deployment-proof/frontend/local-preview.png`.
- AWS CloudFormation stack `mediconnect-dev` is `ROLLBACK_COMPLETE` after an early Cognito template validation error; the template was fixed.
- AWS CloudFormation stack `mediconnect-dev-v2` is rolling back because this new/free-plan account rejected Kinesis with `The AWS Access Key Id needs a subscription for the service`.
- Template has now been changed so `EnableKinesis=false` by default and IoT Core invokes the vitals Lambda directly. Kinesis remains ready behind an opt-in parameter for when the account subscription is activated.
- Next deployment must use a new stack name such as `mediconnect-dev-v3` after `mediconnect-dev-v2` reaches `ROLLBACK_COMPLETE`.

## Architecture target

1. React/Vite patient and clinician dashboard on S3 website hosting.
2. Cognito user pool and client.
3. API Gateway HTTP API plus Lambda appointment API.
4. Aurora PostgreSQL Serverless v2 through the RDS Data API.
5. IoT Core topic rule for synthetic wearable data.
6. Kinesis on-demand stream when the AWS account permits it; direct IoT-to-Lambda fallback meanwhile.
7. Lambda vitals processor, DynamoDB storage, SNS alerts, SQS report queue and DLQ.
8. Comprehend Medical call in Sydney for abnormal synthetic clinical notes.
9. S3 incident reports, ECR repository, ECS/Fargate task definition and CloudWatch logs/alarms.
10. AWS Budget at USD 15/month.

## Roadmap and checkpoints

- [x] Extract the project requirements from the supplied PDF.
- [x] Implement frontend, backend handlers, worker, IaC, tests, README, and license.
- [x] Initialize Git, create public GitHub repository, set description, and push `main`.
- [x] Run Python unit tests and Vite production build.
- [x] Save a local frontend proof screenshot.
- [x] Attempt AWS deployment and diagnose the account-level Kinesis restriction.
- [x] Add an optional-Kinesis/direct-IoT fallback to the template.
- [ ] Validate and push the fallback template.
- [ ] Create `mediconnect-dev-v3` in CloudFormation with `EnableKinesis=false`.
- [ ] Fix any subsequent resource-specific failures and redeploy/update until `CREATE_COMPLETE`.
- [ ] Upload the built frontend in `dist/` to the generated frontend S3 bucket.
- [ ] Verify the public S3 website and API `/health` endpoint.
- [ ] Verify representative AWS resources in CloudFormation and service consoles.
- [ ] Save service-by-service deployment proof screenshots and a final proof index.
- [ ] Update README with live URLs, final resource status, limitations, and cleanup instructions.
- [ ] Commit and push all final documentation and status.
- [ ] Pause the continuation heartbeat automation after completion.

## Immediate continuation procedure

1. In `C:\Users\eashw\Documents\Codex\2026-10-15\d\mediconnect`, review `git status` and `git diff` without discarding user changes.
2. Validate `infra/template.yaml`; run the test/build commands below.
3. Commit the optional-Kinesis change and this handoff, then push `main`.
4. Wait for `mediconnect-dev-v2` to reach `ROLLBACK_COMPLETE` in CloudFormation.
5. Use CloudFormation Template Studio in `ap-south-1`, paste the raw GitHub template, validate it, and create stack `mediconnect-dev-v3` with IAM capabilities. Keep `EnableKinesis=false`.
6. Monitor Events until `CREATE_COMPLETE`. If a resource fails, record the exact event reason here, fix the template, push, and use `mediconnect-dev-v4` or update the active stack as appropriate.
7. After success, copy every CloudFormation output into the final proof index and README.
8. Upload `dist/index.html` and `dist/assets/*` to the frontend bucket, preserving paths and content types.
9. Test the S3 website URL, API health URL, and a safe synthetic vitals invocation.
10. Capture proof for CloudFormation, Cognito, API Gateway/Lambda, RDS, IoT, DynamoDB, SNS/SQS, S3, ECS/ECR, CloudWatch, and Budget. For Kinesis, capture the AWS account restriction and clearly mark it unavailable rather than claiming deployment.

## Verification commands

```powershell
python -m unittest discover -s backend\tests -v
corepack pnpm install --frozen-lockfile
corepack pnpm build
git status --short
git log -5 --oneline
git remote -v
```

## Known risks and fallback decisions

- Kinesis is blocked by AWS account subscription, not by the template. Do not claim it is deployed. Keep the conditional resource and direct IoT fallback.
- Aurora Serverless v2 scale-to-zero can fail for some engine versions. If AWS rejects `MinCapacity: 0`, select a supported engine version or use `0.5`, document the running-cost implication, and remain within the USD 15 cap.
- Account-level S3 public-access blocking may prevent website policy creation. If so, keep report storage private and use a CloudFront/OAC or other low-cost static-hosting adjustment instead of weakening unrelated account settings.
- The SNS email subscription remains pending until the owner confirms the email. Deployment can otherwise complete.
- Fargate should remain at zero desired tasks/on-demand for this demo to control cost.

## Checkpoint log

- 2026-10-15: Implemented and tested the application; pushed the public repository.
- 2026-10-16 00:01 IST: `mediconnect-dev` failed template validation; fixed Cognito `Policies.PasswordPolicy` nesting.
- 2026-10-16 00:04 IST: `mediconnect-dev-v2` started, then Kinesis failed because the account needs a service subscription; rollback began.
- 2026-10-16 00:10 IST: Added `EnableKinesis` condition and direct IoT-to-Lambda fallback; created this continuation handoff.

## Definition of done

The project is complete only when the repository is current, tests/build pass, the maximum supported AWS architecture is `CREATE_COMPLETE`, public frontend and health endpoint are verified, the Kinesis account limitation is honestly documented, proof screenshots are saved, live URLs are in the README, and cost controls remain active.
