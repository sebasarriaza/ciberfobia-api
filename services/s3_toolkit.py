import os
import boto3
import logging
from urllib.parse import urlparse
from botocore.config import Config
from typing import Optional

logger = logging.getLogger(__name__)

def parse_s3_url(s3_url):
    """Parse S3 URL to extract bucket name and (optionally) region."""
    parsed_url = urlparse(s3_url)
    # Extract bucket name from the host or path
    if parsed_url.hostname:
        bucket_name = parsed_url.hostname.split('.')[0]
    else:
        # fallback: s3://bucket/key
        bucket_name = parsed_url.path.lstrip('/').split('/')[0]
    # Try to extract region if present in the host
    region = None
    host_parts = parsed_url.hostname.split('.') if parsed_url.hostname else []
    if len(host_parts) > 1:
        region = host_parts[1]
    return bucket_name, region

def upload_to_s3(file_path: str,
                 bucket_name: str,
                 region: str,
                 endpoint_url: str,
                 access_key: str,
                 secret_key: str,
                 addressing_style: Optional[str] = None,
                 signature_version: Optional[str] = None):
    session = boto3.Session(
        aws_access_key_id=access_key,
        aws_secret_access_key=secret_key,
        region_name=region
    )
    boto_cfg = Config(
        s3={'addressing_style': addressing_style or 'path'},
        signature_version=signature_version or 's3v4'
    )
    client = session.client('s3',
                           endpoint_url=endpoint_url,
                           region_name=region,
                           config=boto_cfg)
    try:
        with open(file_path, 'rb') as data:
            client.upload_fileobj(data, bucket_name, os.path.basename(file_path), ExtraArgs={'ACL': 'public-read'})
        file_url = f"{endpoint_url.rstrip('/')}/{bucket_name}/{os.path.basename(file_path)}"
        return file_url
    except Exception as e:
        logger.error(f"Error uploading file to S3: {e}")
        raise
