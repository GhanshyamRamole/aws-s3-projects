# 🧠 AWS Serverless Intelligent Document Processing (IDP)

![Status](https://img.shields.io/badge/status-active-success.svg)
![AWS](https://img.shields.io/badge/AWS-232F3E?style=for-the-badge&logo=amazon-aws&logoColor=white)
![Python](https://img.shields.io/badge/Python-3.9-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Step Functions](https://img.shields.io/badge/Step%20Functions-FF4F81?style=for-the-badge&logo=amazon-aws&logoColor=white)
![Terraform](https://img.shields.io/badge/Terraform-7B42BC?style=for-the-badge&logo=terraform&logoColor=white)

---

## 📖 Overview

This project implements an **Event-Driven Serverless Intelligent Document Processing (IDP) pipeline** on AWS.

When a document is uploaded to Amazon S3, the system automatically extracts text, detects Personally Identifiable Information (PII), redacts sensitive content, and securely stores the processed output. The workflow is orchestrated using **AWS Step Functions** and leverages **AWS AI services** for scalable and resilient processing.

This project demonstrates **production-ready serverless architecture**, **secure data handling**, and **Infrastructure as Code (IaC)** best practices.

---

## 🏗️ Architecture

The solution follows the **Orchestrator Pattern** using AWS Step Functions.

### Workflow

1. User uploads a document to the **Raw S3 Bucket**
2. S3 event triggers a **Lambda function**
3. Lambda starts a **Step Functions state machine**
4. **Amazon Textract** extracts text from the document
5. **Amazon Comprehend** detects PII
6. Lambda redacts sensitive information
7. Output is securely stored and archived

---

## 📐 Visual Workflow

```mermaid
graph LR
    User -->|Upload| S3Raw[S3 Raw Bucket]
    S3Raw -->|Trigger| LambdaStart[Lambda: Start Execution]
    LambdaStart --> SFN{Step Functions}

    subgraph "AI Processing Pipeline"
        SFN -->|Extract Text| Textract[Amazon Textract]
        Textract -->|Detect PII| Comprehend[Amazon Comprehend]
        Comprehend -->|Redact Data| LambdaRedact[Lambda: Redact]
    end

    LambdaRedact -->|Store Metadata| DDB[(DynamoDB)]
    LambdaRedact -->|Save Redacted File| S3Clean[S3 Processed Bucket]
    LambdaRedact -->|Archive Original| Glacier[S3 Glacier]
🛠️ Tech Stack
Compute: AWS Lambda (Python 3.9)

Orchestration: AWS Step Functions

Storage: Amazon S3, Amazon DynamoDB, Amazon S3 Glacier

AI/ML: Amazon Textract, Amazon Comprehend

Notifications: Amazon SNS

Infrastructure as Code: Terraform

📂 Repository Structure
bash
Copy code
.
├── infra/                    # Terraform infrastructure code
│   ├── main.tf               # Core AWS resources
│   ├── state_machine.tf      # Step Functions definition
│   └── iam.tf                # IAM roles & policies
├── src/                      # Application source code
│   ├── functions/            # Lambda functions
│   │   ├── trigger.py
│   │   └── redact.py
│   └── statemachine/
│       └── workflow.json
├── events/                   # Sample test events
└── README.md
🚀 Getting Started
Prerequisites
AWS CLI configured

Terraform v1.0+

Python 3.9+

Installation
```
git clone https://github.com/your-username/aws-serverless-idp.git
cd aws-serverless-idp
```
```
cd infra
terraform init
terraform apply
```
Confirm the SNS subscription from your email.

🧪 Usage
Upload a document to the raw bucket:

```
aws s3 cp sample_document.jpg s3://<raw-bucket-name>/
```
Monitor execution in the AWS Step Functions Console.

Verify:

Redacted output in Processed S3 Bucket

Metadata entry in DynamoDB

Original file archived in S3 Glacier

🛡️ Security
Least-privilege IAM roles

S3 encryption at rest (SSE-S3)

No hardcoded secrets

Sensitive data archived after processing

🤝 Contributing
Fork the repository

Create a feature branch

Commit your changes

Push to your branch

Open a Pull Request

👤 Author
Ghanshyam Ramole
Cloud & DevOps Engineer

GitHub: https://github.com/GhanshyamRamole
LinkedIn: https://www.linkedin.com/in/ghanshyamramole












