from adas.entity import DataIngestionConfig
import boto3
import sys
from datetime import datetime
import os
from adas.config import *
import shutil
import zipfile
from adas.exception import AdasException
import botocore
from adas.constants import *
from adas.logger import logging
import io
import os

class DataIngestion:
    def __init__(self,config:DataIngestionConfig):
        self.config = config
        self.s3 = boto3.resource('s3')
        self.s3_client = boto3.client('s3')
        self.bucket_name=BUCKET_NAME
    


    def __download_file(self):
        s3=download_pvs_csvs(self.bucket_name,self.config.local_data_folder)

        
    def ingest_data(self):
        self.__download_file()