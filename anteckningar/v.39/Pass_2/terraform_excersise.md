# Exercise: First steps with Terraform on GCP

## 🎯 Objective of the exercise
- Install Terraform and connect it to GCP.
- Understand `main.tf`, `variables.tf`, and `tfvars`.
- Deploy a simple GCP resource (storage bucket).
- Practice the basic workflow: **init → plan → apply → destroy**.

## 1. Install Terraform
1. Download Terraform from [terraform.io/downloads](https://developer.hashicorp.com/terraform/downloads).
2. Unzip and put the `terraform` binary in a folder that is on your PATH:
   - macOS (Homebrew):
     ```bash
     brew install terraform
     ```
   - macOS/Linux (manual):
     ```bash
     unzip terraform_*.zip
     sudo mv terraform /usr/local/bin/terraform
     sudo chmod +x /usr/local/bin/terraform
     ```
   - Windows (manual):
     1) Unzip and place `terraform.exe` in e.g. `C:\terraform`  
     2) Add `C:\terraform` to your PATH (System Properties → Environment Variables), or for current PowerShell session:
     ```powershell
     $env:Path += ";C:\terraform"
     ```
   - WSL users: Do the Linux steps inside WSL and move the binary to `/usr/local/bin`.
3. Verify installation:
   ```bash
   terraform -v
   ```

## 2. Configure access to GCP
1. Install the Google Cloud CLI:
   ```bash
   curl https://sdk.cloud.google.com | bash
   gcloud init
   ```
2. Authenticate with your GCP account:
   ```bash
   gcloud auth application-default login
   ```
   This creates credentials that Terraform will use.
3. Make sure your project ID is correct:
   ```bash
   gcloud config get-value project
   ```

## 3. Create a working directory
```bash
mkdir terraform_gcp && cd terraform_gcp
```

## 4. Write Terraform code
Create three files:

**`main.tf`**
```hcl
provider "google" {
  project = var.project_id
  region  = var.region
}

resource "google_storage_bucket" "raw_bucket" {
  name     = "${var.env}-etl-raw"
  location = var.bucket_location
}
```

**`variables.tf`**
```hcl
variable "project_id" {
  type = string
}

variable "region" {
  type    = string
  default = "us-central1"
}

variable "env" {
  type = string
}

variable "bucket_location" {
  type    = string
  default = "US"
}
```

**`dev.tfvars`**
```hcl
project_id      = "your-gcp-project-id"
region          = ""
env             = "dev"
bucket_location = ""
```

## 5. Run Terraform
1. Initialize:
   ```bash
   terraform init
   ```
2. Preview changes:
   ```bash
   terraform plan -var-file="dev.tfvars"
   ```
3. Apply changes:
   ```bash
   terraform apply -var-file="dev.tfvars"
   ```
4. Verify in the GCP console that your bucket was created.

## 6. Clean up
When finished, remove resources:
```bash
terraform destroy -var-file="dev.tfvars"
```

## 7. Explore the documentation
For more details on available resources, arguments, and examples, explore the provider docs:
- [Google Provider documentation](https://registry.terraform.io/providers/hashicorp/google/latest)