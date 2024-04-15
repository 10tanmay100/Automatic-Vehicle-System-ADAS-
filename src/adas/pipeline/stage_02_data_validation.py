from adas.components import DataIngestion,DataValidation
from adas.config import ConfigurationManager
from adas.logger import logging 
from adas.utils import read_data
from pathlib import Path
import os

STAGE_NAME="Data Validation Stage"

def main():
    # config=ConfigurationManager()
    # data_ingestion_config=config.get_data_ingestion_config()
    # data_ingestion=DataIngestion(config=data_ingestion_config)
    # data_ingestion.ingest_data()
    data_validation=DataValidation()
    print(data_validation.apply_validation())





if __name__=="__main__":
    try:
        logging.info(f">>>>>>> {STAGE_NAME} has started <<<<<<<")
        main()
        logging.info(f">>>>>>> {STAGE_NAME} has ended <<<<<<<")
    except Exception as e:
        raise e