import os
import boto3
from tqdm import tqdm
from adas.constants import *


def download_pvs_csvs(bucket_name, local_path):
    # Create an S3 client
    s3 = boto3.client('s3',aws_access_key_id=AWS_ACCESS_KEY_ID,aws_secret_access_key=AWS_SECRET_KEY_ID)

    # Define the paginator to handle buckets with many objects
    paginator = s3.get_paginator('list_objects_v2')

    # Initialize an empty list to collect all objects to download
    objects_to_download = []

    # Use the paginator to fetch objects
    page_iterator = paginator.paginate(Bucket=bucket_name, Prefix='pvs')

    for page in page_iterator:
        if 'Contents' in page:
            for obj in page['Contents']:
                key = obj['Key']
                # Check if the file is a CSV
                if key.endswith('.csv'):
                    objects_to_download.append(key)

    # Download the files with a progress bar
    for key in tqdm(objects_to_download, desc='Downloading CSVs'):
        local_file_path = os.path.join(local_path, key)
        
        # Create directory structure if it doesn't exist
        if not os.path.exists(os.path.dirname(local_file_path)):
            os.makedirs(os.path.dirname(local_file_path))

        # Download the file
        s3.download_file(bucket_name, key, local_file_path)