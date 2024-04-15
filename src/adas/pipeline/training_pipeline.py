from adas.components import DataIngestion,DataTransformation,DataValidation,ModelTrainer
from adas.config import ConfigurationManager
from adas.logger import logging 
from adas.utils import read_data
from pathlib import Path
import os

STAGE_NAME="Training Pipeline Stage"

def main():
    config=ConfigurationManager()
    data_ingestion_config=config.get_data_ingestion_config()
    data_ingestion=DataIngestion(config=data_ingestion_config)
    data_ingestion.ingest_data()
    data_validation=DataValidation(data_ingestion_config)
    print(data_validation.apply_validation())
    if data_validation.apply_validation():
        data_transformation_config=config.get_data_transformation_config()
        data_transformation=DataTransformation(ingest_config=data_ingestion_config,transform_config=data_transformation_config)
        data_transformation.apply_transformation()
        model_trainer_config=config.get_model_trainer_config()
        model_trainer=ModelTrainer(ingest_config=data_ingestion_config,transform_config=data_transformation_config,config=model_trainer_config)
        model_trainer.train()






if __name__=="__main__":
    try:
        logging.info(f">>>>>>> {STAGE_NAME} has started <<<<<<<")
        main()
        logging.info(f">>>>>>> {STAGE_NAME} has ended <<<<<<<")
    except Exception as e:
        raise e