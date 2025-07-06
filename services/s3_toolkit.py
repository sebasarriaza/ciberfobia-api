import os
import boto3
import logging
from urllib.parse import urlparse

logger = logging.getLogger(__name__)

def parse_s3_url(s3_url):
    """Parse S3 URL to extract bucket name, region, and endpoint URL."""
    parsed_url = urlparse(s3_url)
    
    # Extract bucket name from the host
    bucket_name = parsed_url.hostname.split('.')[0]
    
    # Use S3_REGION env var if defined, else extract from host, else None
    region = os.getenv('S3_REGION')
    if not region:
        host_parts = parsed_url.hostname.split('.') if parsed_url.hostname else []
        region = host_parts[1] if len(host_parts) > 1 else None
    
    # Use endpoint from env if defined, else fallback to DO Spaces
    endpoint_url = os.getenv('S3_ENDPOINT_URL')
    if not endpoint_url and region:
        endpoint_url = f"https://{region}.digitaloceanspaces.com"
    
    return bucket_name, region, endpoint_url

def upload_to_s3(file_path, s3_url, access_key, secret_key):
    # Parse the S3 URL into bucket, region, and endpoint
    bucket_name, region, endpoint_url = parse_s3_url(s3_url)
    
    session = boto3.Session(
        aws_access_key_id=access_key,
        aws_secret_access_key=secret_key,
        region_name=region
    )
    
    client = session.client('s3', endpoint_url=endpoint_url)

    try:
        # Upload the file to the specified S3 bucket
        with open(file_path, 'rb') as data:
            client.upload_fileobj(data, bucket_name, os.path.basename(file_path), ExtraArgs={'ACL': 'public-read'})

        file_url = f"{endpoint_url}/{bucket_name}/{os.path.basename(file_path)}"
        return file_url
    except Exception as e:
        logger.error(f"Error uploading file to S3: {e}")
        raise
