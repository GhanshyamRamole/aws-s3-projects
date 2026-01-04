# ☁️ Serverless S3 Metadata Indexer

![AWS](https://img.shields.io/badge/AWS-232F3E?style=for-the-badge&logo=amazon-aws&logoColor=white)
![Lambda](https://img.shields.io/badge/Lambda-FF9900?style=for-the-badge&logo=aws-lambda&logoColor=white)
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![DynamoDB](https://img.shields.io/badge/DynamoDB-4053D6?style=for-the-badge&logo=amazon-dynamodb&logoColor=white)

## 📖 Overview

This project implements an **Event-Driven Serverless Architecture** on AWS. It automates the process of metadata extraction and storage. When a user uploads a file to an **Amazon S3** bucket, an event triggers an **AWS Lambda** function, which extracts file metadata (name, size, type, upload time) and stores it in an **Amazon DynamoDB** table for quick indexing and querying.

## 🏗️ Architecture

The workflow follows a standard serverless pattern:

1.  **Ingest:** User/App uploads a file to the S3 Bucket.
2.  **Trigger:** S3 `ObjectCreated` event invokes the Lambda function asynchronously.
3.  **Process:** Lambda (Python/Boto3) parses the event JSON and extracts metadata.
4.  **Store:** Lambda writes the metadata item to a DynamoDB table.

![Architecture Diagram](./architecture-image.png)
*(Note: )*

## ⚙️ Prerequisites

Before deploying, ensure you have the following:

* **AWS Account** with appropriate permissions (S3, Lambda, DynamoDB, IAM).
* **AWS CLI** installed and configured locally.
* **Python 3.9+** (if running scripts locally).
* *(Optional)* **Terraform** or **AWS SAM** if using Infrastructure as Code.

## 🚀 Setup & Deployment

### 1. Create the DynamoDB Table
* **Table Name:** `FileMetadata`
* **Partition Key:** `file_id` (String)

### 2. Create the S3 Bucket
* Create a unique bucket (e.g., `my-user-data-bucket-123`).
* Ensure **Block Public Access** is enabled for security.

### 3. Deploy the Lambda Function
1.  Create a new function using the **Python 3.x** runtime.
2.  Paste the code from `lambda_function.py`.
3.  Attach an **IAM Role** with the following permissions:
    * `AmazonDynamoDBFullAccess` (or specific `PutItem` policy)
    * `AWSLambdaBasicExecutionRole` (for CloudWatch Logs)

### 4. Configure S3 Trigger
* Go to your S3 Bucket > **Properties** > **Event Notifications**.
* Create a new event:
    * **Event types:** `Put`, `Post`, `Copy`
    * **Destination:** Select your Lambda function.

## 🧪 How to Test

1.  **Upload a file** to your S3 bucket using the console or CLI:
    ```bash
    aws s3 cp test-image.jpg s3://your-bucket-name/
    ```
2.  **Check CloudWatch Logs** to see if the Lambda function triggered successfully.
3.  **Scan the DynamoDB Table**:
    * You should see a new item with `file_name`, `size`, and `upload_time`.

## 📂 Project Structure

```bash
.
├── lambda_function.py   # The main logic for extracting and storing data
├── architecture.png     # Visual diagram of the workflow
├── requirements.txt     # Python dependencies (e.g., boto3)
└── README.md            # Project documentation
