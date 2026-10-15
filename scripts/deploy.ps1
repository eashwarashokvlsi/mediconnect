param(
  [string]$Region = 'ap-south-1',
  [string]$AccountId = '670099380958',
  [string]$AlertEmail = 'eashwarashokvlsi@gmail.com',
  [string]$StackName = 'mediconnect-dev'
)
$ErrorActionPreference = 'Stop'
$aws = (Get-Command aws -ErrorAction Stop).Source
$identity = & $aws sts get-caller-identity --output json | ConvertFrom-Json
if ($identity.Account -ne $AccountId) { throw "Authenticated to $($identity.Account), expected $AccountId" }
python -m unittest discover backend/tests -v
pnpm install
pnpm build
New-Item -ItemType Directory -Force -Path .artifacts | Out-Null
& $aws s3api head-bucket --bucket "$StackName-artifacts-$AccountId" 2>$null
if ($LASTEXITCODE -ne 0) { & $aws s3 mb "s3://$StackName-artifacts-$AccountId" --region $Region }
& $aws cloudformation package --template-file infra/template.yaml --s3-bucket "$StackName-artifacts-$AccountId" --output-template-file .artifacts/packaged.yaml --region $Region
& $aws cloudformation deploy --template-file .artifacts/packaged.yaml --stack-name $StackName --capabilities CAPABILITY_IAM CAPABILITY_AUTO_EXPAND --parameter-overrides "AlertEmail=$AlertEmail" --region $Region --no-fail-on-empty-changeset
$outputs = & $aws cloudformation describe-stacks --stack-name $StackName --region $Region --query 'Stacks[0].Outputs' --output json
$outputs | Set-Content -Encoding utf8 .artifacts/stack-outputs.json
$frontendBucket = (& $aws cloudformation describe-stack-resource --stack-name $StackName --logical-resource-id FrontendBucket --region $Region --query 'StackResourceDetail.PhysicalResourceId' --output text)
& $aws s3 sync dist "s3://$frontendBucket" --delete --region $Region
Write-Host $outputs
