import os
import boto3
import logging
from urllib.parse import urlparse
from botocore.config import Config as BotoConfig

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

def upload_to_s3(file_path, bucket_name, region, endpoint_url, access_key, secret_key, addressing_style=None, signature_version=None):
    # Use endpoint_url from env or fallback to DO Spaces
    if not endpoint_url:
        if region:
            endpoint_url = f"https://{region}.digitaloceanspaces.com"
        else:
            endpoint_url = "https://nyc3.digitaloceanspaces.com"  # fallback default

    # Prepare boto3 config
    boto_config_kwargs = {}
    if addressing_style:
        boto_config_kwargs['s3'] = {'addressing_style': addressing_style}
    if signature_version:
        boto_config_kwargs['signature_version'] = signature_version
    boto_config = BotoConfig(**boto_config_kwargs) if boto_config_kwargs else None

    session = boto3.Session(
        aws_access_key_id=access_key,
        aws_secret_access_key=secret_key,
        region_name=region
    )

    client_kwargs = {'endpoint_url': endpoint_url}
    if boto_config:
        client_kwargs['config'] = boto_config
    client = session.client('s3', **client_kwargs)

    try:
        # Upload the file to the specified S3 bucket
        with open(file_path, 'rb') as data:
            client.upload_fileobj(data, bucket_name, os.path.basename(file_path), ExtraArgs={'ACL': 'public-read'})

        file_url = f"{endpoint_url}/{bucket_name}/{os.path.basename(file_path)}"
        return file_url
    except Exception as e:
        logger.error(f"Error uploading file to S3: {e}")
        raise
