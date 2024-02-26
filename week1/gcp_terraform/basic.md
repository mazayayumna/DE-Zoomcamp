# GCP and Terraform Basic

## Setting GCP
1) Make a new project -> Service Account
2) FIll details -> Grant Role for Storage, BigQuery, and Compute Admin (later can edit in IAM)
3) Permission to run: Click action -> Manage Keys -> Add key
4) Save json credential to /keys folder, export its path to $GOOGLE_CREDENTIALS
5) Run Terraform command below, you can see the bucket in the cloud storage

## Basic Terraform command
```
terraform fmt
terraform init
terraform plan
terraform apply
terraform destroy
```