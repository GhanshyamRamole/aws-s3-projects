import json
import urllib.parse
import boto3
import os
import uuid
from datetime import datetime

# Initialize AWS clients outside the handler for performance (connection reuse)
s3 = boto3.client('s3')
dynamodb = boto3.resource('dynamodb')

# Best Practice: Use Environment Variables for configuration
# If you didn't set this env var, it defaults to 'FileMetadata'
TABLE_NAME = os.environ.get('TABLE_NAME', 'FileMetadata')

def lambda_handler(event, context):
    """
    Triggered by S3 ObjectCreated Event.
    Extracts metadata and writes to DynamoDB.
    """
    
    # Log the incoming event for debugging in CloudWatch
    print("Received event: " + json.dumps(event, indent=2))

    # Reference the DynamoDB table
    table = dynamodb.Table(TABLE_NAME)

    try:
        # Loop through records (S3 can potentially send multiple records in one event)
        for record in event['Records']:
            
            # 1. Extract Bucket Name and Object Key
            bucket = record['s3']['bucket']['name']
            raw_key = record['s3']['object']['key']
            
            # S3 keys in events are URL encoded (e.g., "My%20File.jpg"). 
            # We must decode them to get the actual filename.
            key = urllib.parse.unquote_plus(raw_key, encoding='utf-8')

            # 2. Fetch additional metadata from S3 (like size and type)
            # We use head_object so we don't download the whole file, just the headers.
            response = s3.head_object(Bucket=bucket, Key=key)
            
            file_size = response['ContentLength']
            content_type = response['ContentType']

            # 3. Construct the DynamoDB Item
            item = {
                'file_id': str(uuid.uuid4()),        # Partition Key (Unique ID)
                'file_name': key,                    # The actual filename
                'bucket_name': bucket,
                'file_size_bytes': file_size,
                'file_type': content_type,
                'upload_timestamp': datetime.utcnow().isoformat(),
                's3_url': f"https://{bucket}.s3.amazonaws.com/{raw_key}"
            }

            # 4. Write to DynamoDB
            table.put_item(Item=item)
            
            print(f"SUCCESS: Indexed {key} into DynamoDB table {TABLE_NAME}")

        return {
            'statusCode': 200,
            'body': json.dumps('Metadata indexing successful')
        }

    except Exception as e:
        print(f"ERROR: Failed to process object from bucket {bucket}.")
        print(e)
        # Raising the exception causes the Lambda to fail, triggering a retry
        raise e
