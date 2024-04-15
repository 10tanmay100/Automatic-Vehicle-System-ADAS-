from adas.constants import *
import sys
import os
from adas.utils import read_yaml,create_directories
from adas.entity import DataIngestionConfig,DataTransformationConfig,ModelTrainerConfig
from adas.exception import AdasException
from datetime import datetime
class ConfigurationManager:
    def __init__(
        self, 
        config_filepath = CONFIG_FILE_PATH):
        self.config = read_yaml(config_filepath)
        create_directories([self.config.artifacts_root])

    def get_data_ingestion_config(self) -> DataIngestionConfig:
        config = self.config.data_ingestion
        try:
            #detecting the current datetime
            now = datetime.now()
            #generating the folder based on the current datetime
            date_time = now.strftime("%m-%d-%Y-%H-%M-%S-%MS")
            #defining the  directory
            dataingestion_dir=os.path.join(config.root_dir,str(date_time))
            create_directories([dataingestion_dir])
            data_ingestion_config = DataIngestionConfig(
                root_dir=config.root_dir,
                S3_bucket_name=BUCKET_NAME,
                local_data_folder=dataingestion_dir,
            )

            return data_ingestion_config
        except Exception as e:
            raise AdasException(e,sys) from e
    def get_data_transformation_config(self):
        try:
            config=self.config.data_transformation
            #detecting the current datetime
            now = datetime.now()
            #generating the folder based on the current datetime
            date_time = now.strftime("%m-%d-%Y-%H-%M-%S-%MS")
            #deining the validate local data file path
            transformed_path=os.path.join(config.root_dir,str(date_time))
            train_transformed_path=os.path.join(transformed_path,"train")
            test_transformed_path=os.path.join(transformed_path,"test")
            transformed_model_path=os.path.join(transformed_path,"model_scaler")

            #creating all directories
            create_directories([train_transformed_path,test_transformed_path,transformed_model_path])

            data_transformation_config=DataTransformationConfig(root_dir=Path(transformed_path),transfromed_train_path=Path(train_transformed_path),transfromed_test_path=Path(test_transformed_path),scaler_model_path=Path(transformed_model_path))

            return data_transformation_config
        except Exception as e:
            raise AdasException(e,sys) from e


    def get_model_trainer_config(self):
        try:
            config=self.config.model_trainer
            #detecting the current datetime
            now = datetime.now()
            #generating the folder based on the current datetime
            date_time = now.strftime("%m-%d-%Y-%H-%M-%S-%MS")
            #deining the validate local data file path
            model_dir_path=os.path.join(config.root_dir,str(date_time))
            

            #creating all directories
            create_directories([model_dir_path])

            model_trainer_config=ModelTrainerConfig(root_dir=Path(model_dir_path))

            return model_trainer_config
        except Exception as e:
            raise AdasException(e,sys) from e
        